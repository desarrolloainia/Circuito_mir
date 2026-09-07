from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from modules.archivos.api.dto import DocumentoDTO
from modules.archivos.domain.Enum.estado_documetno import TipoDocumento
from modules.mir.domain.entities.mir import Solucionado


class CrearMirDTO(BaseModel):
    descripcion: str = Field(min_length=1)
    solucionado: Solucionado
    nombre_empresa: str = Field(min_length=1, max_length=255)
    nombre_persona_empresa: str = Field(min_length=1, max_length=255)
    telefono_empresa: int = Field(ge=0)
    codigo_cliente: str = Field(min_length=1, max_length=100)
    correo_cliente: str = Field(min_length=3, max_length=320)
    fecha_deteccion: date
    tipos_documento: list[TipoDocumento] = Field(default_factory=list)


class ActualizarMirDTO(BaseModel):
    descripcion: str = Field(min_length=1)
    solucionado: Solucionado
    nombre_empresa: str = Field(min_length=1, max_length=255)
    nombre_persona_empresa: str = Field(min_length=1, max_length=255)
    telefono_empresa: int = Field(ge=0)
    codigo_cliente: str = Field(min_length=1, max_length=100)
    correo_cliente: str = Field(min_length=3, max_length=320)
    fecha_deteccion: date
    documento_ids: list[UUID] = Field(default_factory=list)

    @model_validator(mode="after")
    def documentos_sin_repetir(self):
        if len(self.documento_ids) != len(set(self.documento_ids)):
            raise ValueError("documento_ids no puede contener duplicados")
        return self


class MirDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    descripcion: str
    solucionado: Solucionado
    archivos_adjuntos: list[DocumentoDTO]
    nombre_empresa: str
    nombre_persona_empresa: str
    telefono_empresa: int
    codigo_cliente: str
    correo_cliente: str
    fecha_deteccion: date
