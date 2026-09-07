import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from modules.archivos.api.dto import DocumentoDTO, EditarDocumentoDTO
from pydantic import ValidationError

from modules.archivos.application.ports.file_storage import (
    ArchivoSubido,
    FileStorageNotFoundError,
)
from modules.archivos.application.uses_cases.editar_documentos import editar_documento
from modules.archivos.application.uses_cases.eliminar_documento import (
    eliminar_documento,
)
from modules.archivos.application.uses_cases.subir_documento import subir_documento
from modules.archivos.domain.entities.documento import Documento
from modules.archivos.domain.Enum.estado_documetno import TipoDocumento
from modules.archivos.infrastructure.db.entities.documento import DocumentoORM
from modules.archivos.infrastructure.db.persistence.documento_repository import (
    DocumentoRepositorySqlAlchemy,
)
from shared.uow import UnitOfWork


def run(coroutine):
    return asyncio.run(coroutine)


class UowStub:
    def __init__(self, commit_error: Exception | None = None) -> None:
        self.commit = AsyncMock(side_effect=commit_error)
        self.entered = 0
        self.exited = 0

    async def __aenter__(self):
        self.entered += 1
        return self

    async def __aexit__(self, *_):
        self.exited += 1


def documento() -> Documento:
    return Documento(
        nombre="informe.pdf",
        tipo=TipoDocumento.PDF,
        storage_id="storage-1",
        creado_por=uuid4(),
    )


def dependencias_subida(*, save_error=None, commit_error=None, cleanup_error=None):
    storage = SimpleNamespace(
        subir=AsyncMock(
            return_value=ArchivoSubido(
                storage_id="storage-1",
                nombre="informe.pdf",
                tamano_bytes=3,
            )
        ),
        eliminar=AsyncMock(side_effect=cleanup_error),
    )
    repositorio = SimpleNamespace(save=AsyncMock(side_effect=save_error))
    uow = UowStub(commit_error)
    return storage, repositorio, uow


def ejecutar_subida(storage, repositorio, uow):
    return run(
        subir_documento(
            nombre="informe.pdf",
            contenido=b"pdf",
            content_type="application/pdf",
            tipo=TipoDocumento.PDF,
            creado_por=uuid4(),
            storage=storage,
            repositorio=repositorio,
            uow=uow,
        )
    )


def test_subir_documento_guarda_confirma_y_devuelve_documento():
    storage, repositorio, uow = dependencias_subida()
    repositorio.save.side_effect = lambda value: value

    resultado = ejecutar_subida(storage, repositorio, uow)

    assert resultado.storage_id == "storage-1"
    repositorio.save.assert_awaited_once_with(resultado)
    uow.commit.assert_awaited_once()
    storage.eliminar.assert_not_awaited()
    assert (uow.entered, uow.exited) == (1, 1)


@pytest.mark.parametrize("falla_en", ["save", "commit"])
def test_subir_documento_compensa_y_conserva_error_original(falla_en):
    error = RuntimeError(falla_en)
    storage, repositorio, uow = dependencias_subida(
        save_error=error if falla_en == "save" else None,
        commit_error=error if falla_en == "commit" else None,
    )
    if falla_en == "commit":
        repositorio.save.side_effect = lambda value: value

    with pytest.raises(RuntimeError) as capturada:
        ejecutar_subida(storage, repositorio, uow)

    assert capturada.value is error
    storage.eliminar.assert_awaited_once_with("storage-1")


def test_subir_documento_no_oculta_error_si_falla_compensacion():
    error = RuntimeError("save")
    storage, repositorio, uow = dependencias_subida(
        save_error=error,
        cleanup_error=OSError("storage"),
    )

    with pytest.raises(RuntimeError) as capturada:
        ejecutar_subida(storage, repositorio, uow)

    assert capturada.value is error


def test_eliminar_documento_borra_storage_metadata_y_confirma_en_orden():
    doc = documento()
    eventos = []
    storage = SimpleNamespace(
        eliminar=AsyncMock(side_effect=lambda value: eventos.append(("storage", value)))
    )
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=doc),
        delete=AsyncMock(side_effect=lambda value: eventos.append(("metadata", value))),
    )
    uow = UowStub()
    uow.commit.side_effect = lambda: eventos.append(("commit", None))

    run(eliminar_documento(doc.id, storage, repositorio, uow))

    assert eventos == [
        ("storage", doc.storage_id),
        ("metadata", doc.id),
        ("commit", None),
    ]


def test_eliminar_documento_inexistente_es_idempotente():
    documento_id = uuid4()
    storage = SimpleNamespace(eliminar=AsyncMock())
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=None),
        delete=AsyncMock(),
    )
    uow = UowStub()

    run(eliminar_documento(documento_id, storage, repositorio, uow))

    storage.eliminar.assert_not_awaited()
    repositorio.delete.assert_not_awaited()
    uow.commit.assert_not_awaited()


def test_eliminar_documento_limpia_metadata_si_storage_devuelve_404():
    doc = documento()
    storage = SimpleNamespace(
        eliminar=AsyncMock(side_effect=FileStorageNotFoundError("404"))
    )
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=doc),
        delete=AsyncMock(),
    )
    uow = UowStub()

    run(eliminar_documento(doc.id, storage, repositorio, uow))

    repositorio.delete.assert_awaited_once_with(doc.id)
    uow.commit.assert_awaited_once()


def test_eliminar_documento_no_toca_bd_si_storage_falla():
    doc = documento()
    error = OSError("storage")
    storage = SimpleNamespace(eliminar=AsyncMock(side_effect=error))
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=doc),
        delete=AsyncMock(),
    )
    uow = UowStub()

    with pytest.raises(OSError) as capturada:
        run(eliminar_documento(doc.id, storage, repositorio, uow))

    assert capturada.value is error
    repositorio.delete.assert_not_awaited()
    uow.commit.assert_not_awaited()


def test_editar_documento_sin_reemplazo_actualiza_metadatos():
    doc = documento()
    storage = SimpleNamespace(eliminar=AsyncMock())
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=doc),
        update=AsyncMock(side_effect=lambda value: value),
    )
    uow = UowStub()

    resultado = run(
        editar_documento(
            documento_id=doc.id,
            nombre="renombrado.pdf",
            storage=storage,
            repositorio=repositorio,
            uow=uow,
        )
    )

    assert resultado is doc
    assert resultado.nombre == "renombrado.pdf"
    storage.eliminar.assert_not_awaited()
    repositorio.update.assert_awaited_once_with(doc)
    uow.commit.assert_awaited_once()


def test_editar_documento_reemplaza_y_elimina_el_archivo_anterior_en_orden():
    doc = documento()
    eventos = []
    subido = ArchivoSubido("storage-2", "nuevo.docx", 5)
    storage = SimpleNamespace(
        subir=AsyncMock(
            side_effect=lambda *_: (eventos.append("subir"), subido)[1]
        ),
        eliminar=AsyncMock(side_effect=lambda *_: eventos.append("eliminar-anterior")),
    )
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=doc),
        update=AsyncMock(
            side_effect=lambda value: (eventos.append("update"), value)[1]
        ),
    )
    uow = UowStub()
    uow.commit.side_effect = lambda: eventos.append("commit")

    resultado = run(
        editar_documento(
            documento_id=doc.id,
            nombre="nuevo.docx",
            contenido=b"nuevo",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            tipo=TipoDocumento.WORD,
            storage=storage,
            repositorio=repositorio,
            uow=uow,
        )
    )

    assert resultado is doc
    assert (doc.nombre, doc.storage_id, doc.tipo) == (
        "nuevo.docx",
        "storage-2",
        TipoDocumento.WORD,
    )
    assert eventos == ["subir", "update", "commit", "eliminar-anterior"]
    storage.eliminar.assert_awaited_once_with("storage-1")


def test_editar_documento_inexistente_no_sube_archivo():
    storage = SimpleNamespace(subir=AsyncMock(), eliminar=AsyncMock())
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=None),
        update=AsyncMock(),
    )
    uow = UowStub()

    resultado = run(
        editar_documento(
            documento_id=uuid4(),
            nombre="nuevo.pdf",
            contenido=b"nuevo",
            content_type="application/pdf",
            storage=storage,
            repositorio=repositorio,
            uow=uow,
        )
    )

    assert resultado is None
    storage.subir.assert_not_awaited()
    repositorio.update.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.parametrize("falla_en", ["update", "commit"])
def test_editar_documento_compensa_archivo_nuevo_si_falla_bd(falla_en):
    doc = documento()
    error = RuntimeError(falla_en)
    storage = SimpleNamespace(
        subir=AsyncMock(return_value=ArchivoSubido("storage-2", "nuevo.pdf", 5)),
        eliminar=AsyncMock(),
    )
    repositorio = SimpleNamespace(
        get_by_id=AsyncMock(return_value=doc),
        update=AsyncMock(side_effect=error if falla_en == "update" else lambda value: value),
    )
    uow = UowStub(error if falla_en == "commit" else None)

    with pytest.raises(RuntimeError) as capturada:
        run(
            editar_documento(
                documento_id=doc.id,
                nombre="nuevo.pdf",
                contenido=b"nuevo",
                content_type="application/pdf",
                storage=storage,
                repositorio=repositorio,
                uow=uow,
            )
        )

    assert capturada.value is error
    storage.eliminar.assert_awaited_once_with("storage-2")


def test_editar_documento_exige_datos_completos_del_reemplazo():
    with pytest.raises(ValueError, match="nombre y content_type"):
        run(
            editar_documento(
                documento_id=uuid4(),
                contenido=b"nuevo",
                storage=SimpleNamespace(),
                repositorio=SimpleNamespace(
                    get_by_id=AsyncMock(return_value=documento())
                ),
                uow=UowStub(),
            )
        )


def test_editar_documento_dto_valida_reemplazo_y_cambios_vacios():
    with pytest.raises(ValidationError, match="nombre y content_type"):
        EditarDocumentoDTO(contenido=b"nuevo")

    with pytest.raises(ValidationError, match="al menos un cambio"):
        EditarDocumentoDTO()

    assert EditarDocumentoDTO(nombre="renombrado.pdf").nombre == "renombrado.pdf"


def test_documento_dto_acepta_entidad_de_dominio():
    doc = documento()

    dto = DocumentoDTO.model_validate(doc)

    assert dto.model_dump() == {
        "id": doc.id,
        "nombre": doc.nombre,
        "tipo": doc.tipo,
        "storage_id": doc.storage_id,
        "creado_por": doc.creado_por,
    }


def test_repositorio_save_agrega_sin_commit():
    doc = documento()
    uow = SimpleNamespace(
        session=SimpleNamespace(add=Mock(), flush=AsyncMock()), commit=AsyncMock()
    )
    repositorio = DocumentoRepositorySqlAlchemy(uow)

    resultado = run(repositorio.save(doc))

    assert resultado is doc
    assert isinstance(uow.session.add.call_args.args[0], DocumentoORM)
    uow.session.flush.assert_awaited_once()
    uow.commit.assert_not_awaited()


def test_repositorio_update_modifica_sin_commit():
    doc = documento()
    doc_orm = DocumentoORM(
        id=doc.id,
        nombre="anterior.pdf",
        tipo=TipoDocumento.PDF,
        storage_id="storage-anterior",
        creado_por=doc.creado_por,
    )
    session = SimpleNamespace(get=AsyncMock(return_value=doc_orm))
    uow = SimpleNamespace(session=session, commit=AsyncMock())
    repositorio = DocumentoRepositorySqlAlchemy(uow)

    resultado = run(repositorio.update(doc))

    assert resultado is doc
    assert (doc_orm.nombre, doc_orm.storage_id) == (doc.nombre, doc.storage_id)
    uow.commit.assert_not_awaited()


def test_repositorio_get_by_id_y_get_all_devuelven_dominio():
    docs_orm = [
        DocumentoORM(
            id=doc.id,
            nombre=doc.nombre,
            tipo=doc.tipo,
            storage_id=doc.storage_id,
            creado_por=doc.creado_por,
        )
        for doc in (documento(), documento())
    ]
    resultado_id = Mock()
    resultado_id.scalar_one_or_none.return_value = docs_orm[0]
    resultado_lista = Mock()
    resultado_lista.scalars.return_value.all.return_value = docs_orm
    session = SimpleNamespace(execute=AsyncMock(side_effect=[resultado_id, resultado_lista]))
    repositorio = DocumentoRepositorySqlAlchemy(SimpleNamespace(session=session))

    encontrado = run(repositorio.get_by_id(docs_orm[0].id))
    todos = run(repositorio.get_all())

    assert encontrado == documento_desde_orm(docs_orm[0])
    assert todos == [documento_desde_orm(value) for value in docs_orm]


def documento_desde_orm(value: DocumentoORM) -> Documento:
    return Documento(
        id=value.id,
        nombre=value.nombre,
        tipo=value.tipo,
        storage_id=value.storage_id,
        creado_por=value.creado_por,
    )


def test_repositorio_delete_usa_uuid_es_idempotente_y_no_confirma():
    documento_id = uuid4()
    doc_orm = Mock(spec=DocumentoORM)
    session = SimpleNamespace(
        get=AsyncMock(side_effect=[doc_orm, None]),
        delete=AsyncMock(),
    )
    uow = SimpleNamespace(session=session, commit=AsyncMock())
    repositorio = DocumentoRepositorySqlAlchemy(uow)

    run(repositorio.delete(documento_id))
    run(repositorio.delete(documento_id))

    assert session.get.await_args_list[0].args == (DocumentoORM, documento_id)
    session.delete.assert_awaited_once_with(doc_orm)
    uow.commit.assert_not_awaited()


class SessionStub:
    def __init__(self) -> None:
        self.pending = None
        self.persisted = None
        self.events = []

    async def commit(self):
        self.persisted = self.pending
        self.events.append("commit")

    async def rollback(self):
        self.pending = None
        self.events.append("rollback")

    async def close(self):
        self.events.append("close")


def test_uow_commit_explicito_persiste_y_cierra():
    session = SessionStub()
    uow = UnitOfWork(lambda: session)

    async def ejercicio():
        async with uow as entered:
            assert entered is uow
            session.pending = "documento"
            await uow.commit()

    run(ejercicio())

    assert session.persisted == "documento"
    assert session.events == ["commit", "rollback", "close"]


@pytest.mark.parametrize("con_error", [False, True])
def test_uow_sin_commit_revierte_y_cierra(con_error):
    session = SessionStub()
    uow = UnitOfWork(lambda: session)

    async def ejercicio():
        async with uow:
            session.pending = "documento"
            if con_error:
                raise RuntimeError("fallo")

    if con_error:
        with pytest.raises(RuntimeError):
            run(ejercicio())
    else:
        run(ejercicio())

    assert session.pending is None
    assert session.events == ["rollback", "close"]
