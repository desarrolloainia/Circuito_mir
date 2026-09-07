import os
from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command


def test_migracion_upgrade_y_downgrade():
    config = Config(str(Path(__file__).parents[2] / "alembic.ini"))

    command.upgrade(config, "head")
    engine = create_engine(os.environ["DATABASE_URL"])
    try:
        assert set(inspect(engine).get_table_names()) >= {
            "alembic_version",
            "documentos",
            "mir",
            "mir_documentos",
        }

        command.downgrade(config, "base")
        assert inspect(engine).get_table_names() == ["alembic_version"]
    finally:
        engine.dispose()
