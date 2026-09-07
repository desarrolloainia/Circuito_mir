from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import Json

from modules.archivos.application.ports.file_storage import (
    FileStorageError,
    FileStoragePort,
)
from modules.archivos.infrastructure.db.persistence.documento_repository import (
    DocumentoRepositorySqlAlchemy,
)
from modules.archivos.infrastructure.storage.sharepoint.graph_client import (
    SharePointGraphClient,
)
from modules.archivos.infrastructure.storage.sharepoint.schema import SharePointSettings
from modules.archivos.infrastructure.storage.sharepoint.sharepoint_adapter import (
    SharePointFileStorageAdapter,
)
from modules.mir.api.dto import ActualizarMirDTO, CrearMirDTO, MirDTO
from modules.mir.application.use_cases.crear_mir_con_archivos import (
    AdjuntoMir,
    crear_mir_con_archivos,
)
from modules.mir.application.use_cases.crud_mir import (
    actualizar_mir,
    eliminar_mir,
    listar_mir,
    obtener_mir,
)
from modules.mir.domain.repository.mir_repository import (
    DocumentoNoEncontradoError,
    DocumentoYaAsignadoError,
    MirNoEncontradaError,
)
from modules.mir.infrastructure.persistence.mir_repository import (
    MirRepositorySqlAlchemy,
)
from shared.uow import UnitOfWork

router = APIRouter(prefix="/mir", tags=["MIR"])

# ponytail: replace this sentinel with the authenticated user's UUID when auth exists.
USUARIO_TEMPORAL_ID = UUID("00000000-0000-0000-0000-000000000001")


def get_uow() -> UnitOfWork:
    return UnitOfWork()


def get_storage() -> FileStoragePort:
    return SharePointFileStorageAdapter(SharePointGraphClient(SharePointSettings()))  # pyright: ignore[reportCallIssue]


def error_http(error: Exception) -> HTTPException:
    if isinstance(error, MirNoEncontradaError):
        return HTTPException(status.HTTP_404_NOT_FOUND, str(error))
    if isinstance(error, DocumentoYaAsignadoError):
        return HTTPException(status.HTTP_409_CONFLICT, str(error))
    if isinstance(error, DocumentoNoEncontradoError):
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(error))
    return HTTPException(status.HTTP_502_BAD_GATEWAY, str(error))


@router.post("", response_model=MirDTO, status_code=status.HTTP_201_CREATED)
async def crear(
    datos: Annotated[Json[CrearMirDTO], Form()],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    storage: Annotated[FileStoragePort, Depends(get_storage)],
    archivos: Annotated[list[UploadFile] | None, File()] = None,
) -> MirDTO:
    archivos = archivos or []

    if len(archivos) != len(datos.tipos_documento):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe indicarse un tipo por cada archivo",
        )

    adjuntos = [
        AdjuntoMir(
            archivo.filename or "archivo",
            await archivo.read(),
            archivo.content_type or "application/octet-stream",
            tipo,
        )
        for archivo, tipo in zip(
            archivos,
            datos.tipos_documento,
            strict=True,
        )
    ]

    try:
        mir = await crear_mir_con_archivos(
            **datos.model_dump(exclude={"tipos_documento"}),
            creado_por=USUARIO_TEMPORAL_ID,
            adjuntos=adjuntos,
            storage=storage,
            documento_repositorio=DocumentoRepositorySqlAlchemy(uow),
            mir_repositorio=MirRepositorySqlAlchemy(uow),
            uow=uow,
        )
    except (
        DocumentoNoEncontradoError,
        DocumentoYaAsignadoError,
        FileStorageError,
    ) as error:
        raise error_http(error) from error

    return MirDTO.model_validate(mir)


@router.get("", response_model=list[MirDTO])
async def listar(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> list[MirDTO]:
    resultado = await listar_mir(MirRepositorySqlAlchemy(uow), uow)
    return [MirDTO.model_validate(mir) for mir in resultado]


@router.get("/{mir_id}", response_model=MirDTO)
async def obtener(
    mir_id: UUID, uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> MirDTO:
    try:
        mir = await obtener_mir(mir_id, MirRepositorySqlAlchemy(uow), uow)
    except MirNoEncontradaError as error:
        raise error_http(error) from error
    return MirDTO.model_validate(mir)


@router.put("/{mir_id}", response_model=MirDTO)
async def actualizar(
    mir_id: UUID,
    datos: ActualizarMirDTO,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MirDTO:
    try:
        mir = await actualizar_mir(
            mir_id=mir_id,
            **datos.model_dump(),
            mir_repositorio=MirRepositorySqlAlchemy(uow),
            documento_repositorio=DocumentoRepositorySqlAlchemy(uow),
            uow=uow,
        )
    except (
        MirNoEncontradaError,
        DocumentoNoEncontradoError,
        DocumentoYaAsignadoError,
    ) as error:
        raise error_http(error) from error
    return MirDTO.model_validate(mir)


@router.delete("/{mir_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(
    mir_id: UUID, uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> None:
    try:
        await eliminar_mir(mir_id, MirRepositorySqlAlchemy(uow), uow)
    except MirNoEncontradaError as error:
        raise error_http(error) from error
