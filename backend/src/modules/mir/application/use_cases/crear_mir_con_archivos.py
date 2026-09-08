import logging
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from modules.archivos.application.ports.file_storage import FileStoragePort
from modules.archivos.application.uses_cases.subir_documento import subir_documento
from modules.archivos.domain.Enum.estado_documetno import TipoDocumento
from modules.archivos.domain.repository.documento_repository import DocumentoRepository
from modules.mir.domain.entities.mir import Mir, Prioridad, Solucionado
from modules.mir.domain.repository.mir_repository import MirRepository
from shared.uow import UnitOfWork

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AdjuntoMir:
    nombre: str
    contenido: bytes
    content_type: str
    tipo: TipoDocumento


async def crear_mir_con_archivos(
    *,
    descripcion: str,
    solucionado: Solucionado,
    nombre_empresa: str,
    prioridad: Prioridad,
    nombre_persona_empresa: str,
    telefono_empresa: int,
    codigo_cliente: str,
    correo_cliente: str,
    fecha_deteccion: date,
    creado_por: UUID,
    adjuntos: list[AdjuntoMir],
    storage: FileStoragePort,
    documento_repositorio: DocumentoRepository,
    mir_repositorio: MirRepository,
    uow: UnitOfWork,
) -> Mir:
    documentos = []
    try:
        async with uow:
            for adjunto in adjuntos:
                documentos.append(
                    await subir_documento(
                        nombre=adjunto.nombre,
                        contenido=adjunto.contenido,
                        content_type=adjunto.content_type,
                        tipo=adjunto.tipo,
                        creado_por=creado_por,
                        storage=storage,
                        repositorio=documento_repositorio,
                        uow=uow,
                        gestionar_transaccion=False,
                    )
                )

            mir = Mir(
                descripcion=descripcion,
                solucionado=solucionado,
                archivos_adjuntos=documentos,
                nombre_empresa=nombre_empresa,
                prioridad=prioridad,
                nombre_persona_empresa=nombre_persona_empresa,
                telefono_empresa=telefono_empresa,
                codigo_cliente=codigo_cliente,
                correo_cliente=correo_cliente,
                fecha_deteccion=fecha_deteccion,
            )
            await mir_repositorio.create_mir(mir)
            await uow.commit()
            return mir
    except Exception:
        for documento in reversed(documentos):
            try:
                await storage.eliminar(documento.storage_id)
            except Exception:
                logger.exception(
                    "No se pudo compensar storage_id=%s", documento.storage_id
                )
        raise
