import uuid
from datetime import date

from sqlalchemy import BigInteger, Column, Date, ForeignKey, String, Table, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modules.archivos.infrastructure.db.entities.documento import DocumentoORM
from modules.mir.domain.entities.mir import Prioridad, Solucionado
from shared.database import Base

mir_documentos = Table(
    "mir_documentos",
    Base.metadata,
    Column(
        "mir_id",
        UUID(as_uuid=True),
        ForeignKey("mir.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "documento_id",
        UUID(as_uuid=True),
        ForeignKey("documentos.id", ondelete="RESTRICT"),
        primary_key=True,
        unique=True,
    ),
)


class MirORM(Base):
    __tablename__ = "mir"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    solucionado: Mapped[Solucionado] = mapped_column(
        SqlEnum(Solucionado, name="solucionado"), nullable=False
    )
    nombre_empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    prioridad: Mapped[Prioridad] = mapped_column(
        SqlEnum(Prioridad, name="prioridad"), nullable=False
    )
    nombre_persona_empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono_empresa: Mapped[int] = mapped_column(BigInteger, nullable=False)
    codigo_cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    correo_cliente: Mapped[str] = mapped_column(String(320), nullable=False)
    fecha_deteccion: Mapped[date] = mapped_column(Date, nullable=False)
    archivos_adjuntos: Mapped[list[DocumentoORM]] = relationship(
        secondary=mir_documentos,
        lazy="selectin",
        passive_deletes=True,
    )
