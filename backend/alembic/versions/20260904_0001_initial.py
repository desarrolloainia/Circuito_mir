"""Esquema inicial de documentos y MIR."""

import sqlalchemy as sa

from alembic import op

revision = "20260904_0001"
down_revision = None
branch_labels = None
depends_on = None

tipo_documento = sa.Enum(
    "PDF", "WORD", "EXCEL", "IMAGEN", "OTRO", name="tipo_documento"
)
solucionado = sa.Enum("SI", "NO", name="solucionado")


def upgrade() -> None:
    op.create_table(
        "documentos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("tipo", tipo_documento, nullable=False),
        sa.Column("storage_id", sa.String(), nullable=False),
        sa.Column("creado_por", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mir",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("solucionado", solucionado, nullable=False),
        sa.Column("nombre_empresa", sa.String(255), nullable=False),
        sa.Column("nombre_persona_empresa", sa.String(255), nullable=False),
        sa.Column("telefono_empresa", sa.BigInteger(), nullable=False),
        sa.Column("codigo_cliente", sa.String(100), nullable=False),
        sa.Column("correo_cliente", sa.String(320), nullable=False),
        sa.Column("fecha_deteccion", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mir_documentos",
        sa.Column("mir_id", sa.Uuid(), nullable=False),
        sa.Column("documento_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["documento_id"], ["documentos.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["mir_id"], ["mir.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("mir_id", "documento_id"),
        sa.UniqueConstraint("documento_id"),
    )


def downgrade() -> None:
    op.drop_table("mir_documentos")
    op.drop_table("mir")
    op.drop_table("documentos")
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        solucionado.drop(bind, checkfirst=True)
        tipo_documento.drop(bind, checkfirst=True)
