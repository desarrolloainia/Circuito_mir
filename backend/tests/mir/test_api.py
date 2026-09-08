import json
from datetime import date
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import app
from modules.mir.api.dto import ActualizarMirDTO
from modules.mir.api.router import USUARIO_TEMPORAL_ID, get_storage, get_uow
from modules.mir.domain.entities.mir import Mir, Prioridad, Solucionado


def test_api_expone_crud_mir():
    respuesta = TestClient(app).get("/openapi.json")
    assert respuesta.status_code == 200
    rutas = {
        (ruta, metodo.upper())
        for ruta, operaciones in respuesta.json()["paths"].items()
        for metodo in operaciones
    }
    assert {
        ("/mir", "POST"),
        ("/mir", "GET"),
        ("/mir/{mir_id}", "GET"),
        ("/mir/{mir_id}", "PUT"),
        ("/mir/{mir_id}", "DELETE"),
    } <= rutas


def test_crear_mir_acepta_datos_json_y_archivos_multipart(monkeypatch):
    creada = Mir(
        descripcion="Una descripcion suficientemente larga",
        solucionado=Solucionado.NO,
        archivos_adjuntos=[],
        nombre_empresa="Empresa",
        prioridad=Prioridad.ALTA,
        nombre_persona_empresa="Ada",
        telefono_empresa=600123123,
        codigo_cliente="CLI-1",
        correo_cliente="ada@example.com",
        fecha_deteccion=date(2026, 9, 4),
    )
    crear = AsyncMock(return_value=creada)
    monkeypatch.setattr("modules.mir.api.router.crear_mir_con_archivos", crear)
    app.dependency_overrides[get_uow] = object
    app.dependency_overrides[get_storage] = object

    try:
        respuesta = TestClient(app).post(
            "/mir",
            data={
                "datos": json.dumps(
                    {
                        "descripcion": creada.descripcion,
                        "solucionado": "no",
                        "nombre_empresa": creada.nombre_empresa,
                        "prioridad": creada.prioridad.value,
                        "nombre_persona_empresa": creada.nombre_persona_empresa,
                        "telefono_empresa": creada.telefono_empresa,
                        "codigo_cliente": creada.codigo_cliente,
                        "correo_cliente": creada.correo_cliente,
                        "fecha_deteccion": creada.fecha_deteccion.isoformat(),
                        "tipos_documento": ["pdf"],
                    }
                )
            },
            files=[("archivos", ("evidencia.pdf", b"pdf", "application/pdf"))],
        )
    finally:
        app.dependency_overrides.clear()

    assert respuesta.status_code == 201
    llamada = crear.await_args
    assert llamada is not None
    argumentos = llamada.kwargs
    assert argumentos["creado_por"] == USUARIO_TEMPORAL_ID
    assert [(a.nombre, a.contenido, a.tipo.value) for a in argumentos["adjuntos"]] == [
        ("evidencia.pdf", b"pdf", "pdf")
    ]


def test_actualizar_mir_dto_rechaza_documentos_repetidos():
    documento_id = uuid4()
    with pytest.raises(ValidationError, match="duplicados"):
        ActualizarMirDTO(
            descripcion="Fallo",
            solucionado=Solucionado.NO,
            nombre_empresa="Empresa",
            prioridad=Prioridad.MEDIA,
            nombre_persona_empresa="Ada",
            telefono_empresa=600123123,
            codigo_cliente="CLI-1",
            correo_cliente="ada@example.com",
            fecha_deteccion=date(2026, 9, 4),
            documento_ids=[documento_id, documento_id],
        )
