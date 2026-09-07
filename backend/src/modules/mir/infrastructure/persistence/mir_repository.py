from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from modules.archivos.infrastructure.db.entities.documento import DocumentoORM
from modules.archivos.infrastructure.db.persistence.documento_repository import (
    to_domain,
)
from modules.mir.domain.entities.mir import Mir
from modules.mir.domain.repository.mir_repository import (
    DocumentoNoEncontradoError,
    DocumentoYaAsignadoError,
    MirNoEncontradaError,
)
from modules.mir.infrastructure.entities.mir import MirORM, mir_documentos
from shared.uow import UnitOfWork


def _to_domain(mir: MirORM) -> Mir:
    return Mir(
        id=mir.id,
        descripcion=mir.descripcion,
        solucionado=mir.solucionado,
        archivos_adjuntos=[to_domain(documento) for documento in mir.archivos_adjuntos],
        nombre_empresa=mir.nombre_empresa,
        nombre_persona_empresa=mir.nombre_persona_empresa,
        telefono_empresa=mir.telefono_empresa,
        codigo_cliente=mir.codigo_cliente,
        correo_cliente=mir.correo_cliente,
        fecha_deteccion=mir.fecha_deteccion,
    )


class MirRepositorySqlAlchemy:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def _documentos(
        self, mir: Mir, *, excluir_mir_id: UUID | None = None
    ) -> list[DocumentoORM]:
        ids = [documento.id for documento in mir.archivos_adjuntos]
        if len(ids) != len(set(ids)):
            raise DocumentoYaAsignadoError("Un documento está repetido en la MIR")
        if not ids:
            return []

        documentos = list(
            (
                await self.uow.session.execute(
                    select(DocumentoORM).where(DocumentoORM.id.in_(ids))
                )
            )
            .scalars()
            .all()
        )
        encontrados = {documento.id for documento in documentos}
        if faltantes := set(ids) - encontrados:
            raise DocumentoNoEncontradoError(
                f"Documentos no encontrados: {', '.join(map(str, faltantes))}"
            )

        asignados = select(mir_documentos.c.documento_id).where(
            mir_documentos.c.documento_id.in_(ids)
        )
        if excluir_mir_id is not None:
            asignados = asignados.where(mir_documentos.c.mir_id != excluir_mir_id)
        if (await self.uow.session.execute(asignados)).first():
            raise DocumentoYaAsignadoError(
                "Uno de los documentos ya pertenece a otra MIR"
            )
        return documentos

    async def create_mir(self, mir: Mir) -> Mir:
        mir_orm = MirORM(
            id=mir.id,
            descripcion=mir.descripcion,
            solucionado=mir.solucionado,
            archivos_adjuntos=await self._documentos(mir),
            nombre_empresa=mir.nombre_empresa,
            nombre_persona_empresa=mir.nombre_persona_empresa,
            telefono_empresa=mir.telefono_empresa,
            codigo_cliente=mir.codigo_cliente,
            correo_cliente=mir.correo_cliente,
            fecha_deteccion=mir.fecha_deteccion,
        )
        self.uow.session.add(mir_orm)
        try:
            await self.uow.session.flush()
        except IntegrityError as error:
            raise DocumentoYaAsignadoError(
                "Uno de los documentos ya pertenece a otra MIR"
            ) from error
        return mir

    async def get_mir_by_id(self, mir_id: UUID) -> Mir | None:
        mir = (
            await self.uow.session.execute(select(MirORM).where(MirORM.id == mir_id))
        ).scalar_one_or_none()
        return _to_domain(mir) if mir else None

    async def get_all_mir(self) -> list[Mir]:
        resultado = await self.uow.session.execute(select(MirORM))
        return [_to_domain(mir) for mir in resultado.scalars().all()]

    async def update_mir(self, mir: Mir) -> Mir:
        mir_orm = (
            await self.uow.session.execute(select(MirORM).where(MirORM.id == mir.id))
        ).scalar_one_or_none()
        if mir_orm is None:
            raise MirNoEncontradaError(f"MIR con id {mir.id} no encontrada")

        mir_orm.descripcion = mir.descripcion
        mir_orm.solucionado = mir.solucionado
        mir_orm.nombre_empresa = mir.nombre_empresa
        mir_orm.nombre_persona_empresa = mir.nombre_persona_empresa
        mir_orm.telefono_empresa = mir.telefono_empresa
        mir_orm.codigo_cliente = mir.codigo_cliente
        mir_orm.correo_cliente = mir.correo_cliente
        mir_orm.fecha_deteccion = mir.fecha_deteccion
        mir_orm.archivos_adjuntos = await self._documentos(mir, excluir_mir_id=mir.id)
        try:
            await self.uow.session.flush()
        except IntegrityError as error:
            raise DocumentoYaAsignadoError(
                "Uno de los documentos ya pertenece a otra MIR"
            ) from error
        return mir

    async def delete_mir(self, mir_id: UUID) -> None:
        mir = await self.uow.session.get(MirORM, mir_id)
        if mir is None:
            raise MirNoEncontradaError(f"MIR con id {mir_id} no encontrada")
        await self.uow.session.delete(mir)
        await self.uow.session.flush()
