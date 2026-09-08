"""Añade la prioridad de las MIR."""

import sqlalchemy as sa

from alembic import op

revision = "20260908_0003"
down_revision = "20260907_0002"
branch_labels = None
depends_on = None

prioridad = sa.Enum("ALTA", "MEDIA", "BAJA", name="prioridad")


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        prioridad.create(bind, checkfirst=True)
    op.add_column(
        "mir",
        sa.Column(
            "prioridad",
            prioridad,
            server_default="BAJA",
            nullable=False,
        ),
    )
    op.alter_column("mir", "prioridad", server_default=None)


def downgrade() -> None:
    op.drop_column("mir", "prioridad")
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        prioridad.drop(bind, checkfirst=True)
