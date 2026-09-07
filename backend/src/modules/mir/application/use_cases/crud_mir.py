from datetime import date
from uuid import UUID

from modules.archivos.domain.repository.documento_repository import DocumentoRepository
from modules.mir.domain.entities.mir import Mir, Solucionado
from modules.mir.domain.repository.mir_repository import (
    DocumentoNoEncontradoError,
    MirNoEncontradaError,
    MirRepository,
)
from shared.uow import UnitOfWork


async def obtener_mir(
    mir_id: UUID, repositorio: MirRepository, uow: UnitOfWork
) -> Mir:
    async with uow:
        mir = await repositorio.get_mir_by_id(mir_id)
        if mir is None:
            raise MirNoEncontradaError(f"MIR con id {mir_id} no encontrada")
        return mir


async def listar_mir(repositorio: MirRepository, uow: UnitOfWork) -> list[Mir]:
    async with uow:
        return await repositorio.get_all_mir()


async def actualizar_mir(
    *,
    mir_id: UUID,
    descripcion: str,
    solucionado: Solucionado,
    nombre_empresa: str,
    nombre_persona_empresa: str,
    telefono_empresa: int,
    codigo_cliente: str,
    correo_cliente: str,
    fecha_deteccion: date,
    documento_ids: list[UUID],
    mir_repositorio: MirRepository,
    documento_repositorio: DocumentoRepository,
    uow: UnitOfWork,
) -> Mir:
    async with uow:
        documentos = []
        for documento_id in documento_ids:
            documento = await documento_repositorio.get_by_id(documento_id)
            if documento is None:
                raise DocumentoNoEncontradoError(
                    f"Documento con id {documento_id} no encontrado"
                )
            documentos.append(documento)

        mir = Mir(
            id=mir_id,
            descripcion=descripcion,
            solucionado=solucionado,
            archivos_adjuntos=documentos,
            nombre_empresa=nombre_empresa,
            nombre_persona_empresa=nombre_persona_empresa,
            telefono_empresa=telefono_empresa,
            codigo_cliente=codigo_cliente,
            correo_cliente=correo_cliente,
            fecha_deteccion=fecha_deteccion,
        )
        await mir_repositorio.update_mir(mir)
        await uow.commit()
        return mir


async def eliminar_mir(
    mir_id: UUID, repositorio: MirRepository, uow: UnitOfWork
) -> None:
    async with uow:
        await repositorio.delete_mir(mir_id)
        await uow.commit()
