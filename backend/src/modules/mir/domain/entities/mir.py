from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from uuid import UUID, uuid4

from ....archivos.domain.entities.documento import Documento


class estado(Enum):
    ABIERTO = "abierto"
    EN_PROCESADO = "en_procesado"
    CERRADO = "cerrado"


class Prioridad(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

class TipoMir(Enum):
    MEJORA = "Mejora"
    INCIDENCIA = "Incidencia"
    RECLAMACION = "Reclamacion"


@dataclass
class Mir:
    descripcion: str
    estado: estado
    archivos_adjuntos: list[Documento]
    nombre_empresa: str
    prioridad: Prioridad
    tipo: TipoMir
    nombre_persona_empresa: str
    telefono_empresa: int
    codigo_cliente: str
    correo_cliente: str
    fecha_deteccion: date
    id: UUID = field(default_factory=uuid4)
