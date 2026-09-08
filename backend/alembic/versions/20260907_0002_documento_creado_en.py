"""Añade la fecha y hora de subida de los documentos."""

import sqlalchemy as sa

from alembic import op

revision = "20260907_0002"
down_revision = "20260904_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "documentos",
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("documentos", "creado_en")
