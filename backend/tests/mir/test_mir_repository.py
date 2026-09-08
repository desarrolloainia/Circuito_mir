import asyncio
import os
from dataclasses import replace
from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from modules.archivos.domain.entities.documento import Documento
from modules.archivos.domain.Enum.estado_documetno import TipoDocumento
from modules.archivos.infrastructure.db.entities.documento import DocumentoORM
from modules.archivos.infrastructure.db.persistence.documento_repository import (
    DocumentoRepositorySqlAlchemy,
)
from modules.mir.domain.entities.mir import Mir, Prioridad, Solucionado
from modules.mir.domain.repository.mir_repository import (
    DocumentoNoEncontradoError,
    DocumentoYaAsignadoError,
    MirNoEncontradaError,
)
from modules.mir.infrastructure.entities.mir import mir_documentos
from modules.mir.infrastructure.persistence.mir_repository import (
    MirRepositorySqlAlchemy,
)
from shared.database import Base
from shared.uow import UnitOfWork


def run(coroutine):
    return asyncio.run(coroutine)


def documento(nombre: str) -> Documento:
    return Documento(nombre, TipoDocumento.PDF, f"storage-{nombre}", uuid4())


def mir(documentos: list[Documento], **cambios) -> Mir:
    base = Mir(
        descripcion="Fallo de circuito",
        solucionado=Solucionado.NO,
        archivos_adjuntos=documentos,
        nombre_empresa="Empresa",
        prioridad=Prioridad.ALTA,
        nombre_persona_empresa="Ada",
        telefono_empresa=600123123,
        codigo_cliente="CLI-1",
        correo_cliente="ada@example.com",
        fecha_deteccion=date(2026, 9, 4),
    )
    return replace(base, **cambios)


async def en_bd(ejercicio):
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL es obligatoria para pruebas destructivas")
    engine = create_async_engine(database_url)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    try:
        await ejercicio(async_sessionmaker(engine, expire_on_commit=False))
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
        await engine.dispose()


def test_crud_carga_documentos_reemplaza_enlaces_y_conserva_documentos():
    async def ejercicio(factory):
        uow = UnitOfWork(factory)
        async with uow:
            documentos = [
                documento("uno.pdf"),
                documento("dos.pdf"),
                documento("tres.pdf"),
            ]
            docs = DocumentoRepositorySqlAlchemy(uow)
            repo = MirRepositorySqlAlchemy(uow)
            for doc in documentos:
                await docs.save(doc)

            creada = mir(documentos[:2])
            await repo.create_mir(creada)
            await uow.commit()
            recuperada = await repo.get_mir_by_id(creada.id)
            assert recuperada == creada
            assert (await repo.get_all_mir()) == [creada]

            actualizada = replace(
                creada,
                descripcion="Resuelto",
                solucionado=Solucionado.SI,
                archivos_adjuntos=documentos[1:],
            )
            await repo.update_mir(actualizada)
            await uow.commit()
            assert await repo.get_mir_by_id(creada.id) == actualizada

            await repo.delete_mir(creada.id)
            await uow.commit()
            assert await repo.get_mir_by_id(creada.id) is None
            assert (
                await uow.session.scalar(select(func.count()).select_from(DocumentoORM))
            ) == 3
            assert (
                await uow.session.scalar(
                    select(func.count()).select_from(mir_documentos)
                )
            ) == 0

    run(en_bd(ejercicio))


def test_documento_no_puede_pertenecer_a_dos_mir():
    async def ejercicio(factory):
        uow = UnitOfWork(factory)
        async with uow:
            doc = documento("unico.pdf")
            await DocumentoRepositorySqlAlchemy(uow).save(doc)
            repo = MirRepositorySqlAlchemy(uow)
            await repo.create_mir(mir([doc]))
            with pytest.raises(DocumentoYaAsignadoError):
                await repo.create_mir(mir([doc]))

    run(en_bd(ejercicio))


def test_repositorio_informa_mir_y_documento_inexistentes():
    async def ejercicio(factory):
        uow = UnitOfWork(factory)
        async with uow:
            repo = MirRepositorySqlAlchemy(uow)
            with pytest.raises(DocumentoNoEncontradoError):
                await repo.create_mir(mir([documento("ausente.pdf")]))
            with pytest.raises(MirNoEncontradaError):
                await repo.update_mir(mir([], id=uuid4()))
            with pytest.raises(MirNoEncontradaError):
                await repo.delete_mir(uuid4())

    run(en_bd(ejercicio))
