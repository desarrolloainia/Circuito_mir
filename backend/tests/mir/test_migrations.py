import os
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command


def test_migracion_upgrade_y_downgrade(monkeypatch):
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL es obligatoria para pruebas destructivas")
    monkeypatch.setenv("DATABASE_URL", database_url)
    config = Config(str(Path(__file__).parents[2] / "alembic.ini"))

    command.upgrade(config, "head")
    engine = create_engine(database_url)
    try:
        assert set(inspect(engine).get_table_names()) >= {
            "alembic_version",
            "documentos",
            "mir",
            "mir_documentos",
        }
        assert "creado_en" in {
            column["name"] for column in inspect(engine).get_columns("documentos")
        }
        assert "prioridad" in {
            column["name"] for column in inspect(engine).get_columns("mir")
        }

        command.downgrade(config, "base")
        assert inspect(engine).get_table_names() == ["alembic_version"]
    finally:
        engine.dispose()
