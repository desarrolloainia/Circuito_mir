import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from modules.archivos.application.ports.file_storage import ArchivoSubido
from modules.archivos.domain.Enum.estado_documetno import TipoDocumento
from modules.mir.application.use_cases.crear_mir_con_archivos import (
    AdjuntoMir,
    crear_mir_con_archivos,
)
from modules.mir.domain.entities.mir import Prioridad, Solucionado


def run(coroutine):
    return asyncio.run(coroutine)


class UowStub:
    def __init__(self, commit_error=None):
        self.commit = AsyncMock(side_effect=commit_error)
        self.rollback = AsyncMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.rollback()


def ejecutar(*, upload_error=None, save_error=None, mir_error=None, commit_error=None):
    subidos = iter(
        [
            ArchivoSubido("storage-1", "uno.pdf", 3),
            ArchivoSubido("storage-2", "dos.pdf", 3),
        ]
    )
    storage = SimpleNamespace(
        subir=AsyncMock(side_effect=upload_error or (lambda *_: next(subidos))),
        eliminar=AsyncMock(),
    )
    documentos = SimpleNamespace(
        save=AsyncMock(side_effect=save_error or (lambda x: x))
    )
    mir_repo = SimpleNamespace(create_mir=AsyncMock(side_effect=mir_error))
    uow = UowStub(commit_error)
    llamada = crear_mir_con_archivos(
        descripcion="Fallo",
        solucionado=Solucionado.NO,
        nombre_empresa="Empresa",
        prioridad=Prioridad.MEDIA,
        nombre_persona_empresa="Ada",
        telefono_empresa=600123123,
        codigo_cliente="CLI-1",
        correo_cliente="ada@example.com",
        fecha_deteccion=date(2026, 9, 4),
        creado_por=uuid4(),
        adjuntos=[
            AdjuntoMir("uno.pdf", b"uno", "application/pdf", TipoDocumento.PDF),
            AdjuntoMir("dos.pdf", b"dos", "application/pdf", TipoDocumento.PDF),
        ],
        storage=storage,
        documento_repositorio=documentos,
        mir_repositorio=mir_repo,
        uow=uow,
    )
    return llamada, storage, documentos, mir_repo, uow


def test_crea_mir_y_confirma_una_vez():
    llamada, storage, documentos, mir_repo, uow = ejecutar()

    resultado = run(llamada)

    assert [doc.storage_id for doc in resultado.archivos_adjuntos] == [
        "storage-1",
        "storage-2",
    ]
    assert documentos.save.await_count == 2
    mir_repo.create_mir.assert_awaited_once_with(resultado)
    uow.commit.assert_awaited_once()
    storage.eliminar.assert_not_awaited()


@pytest.mark.parametrize("falla_en", ["upload", "documento", "mir", "commit"])
def test_error_revierte_y_compensa_sin_ocultar_error(falla_en):
    error = RuntimeError(falla_en)
    opciones = {
        "upload_error": error if falla_en == "upload" else None,
        "save_error": error if falla_en == "documento" else None,
        "mir_error": error if falla_en == "mir" else None,
        "commit_error": error if falla_en == "commit" else None,
    }
    llamada, storage, _, _, uow = ejecutar(**opciones)

    with pytest.raises(RuntimeError) as capturada:
        run(llamada)

    assert capturada.value is error
    uow.rollback.assert_awaited_once()
    esperadas = 0 if falla_en == "upload" else (1 if falla_en == "documento" else 2)
    assert storage.eliminar.await_count == esperadas


def test_fallo_de_compensacion_conserva_error_original():
    error = RuntimeError("mir")
    llamada, storage, _, _, _ = ejecutar(mir_error=error)
    storage.eliminar.side_effect = OSError("SharePoint")

    with pytest.raises(RuntimeError) as capturada:
        run(llamada)

    assert capturada.value is error
