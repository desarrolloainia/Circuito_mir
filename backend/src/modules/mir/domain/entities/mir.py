from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from uuid import UUID, uuid4

from ....archivos.domain.entities.documento import Documento


class Solucionado(Enum):
    SI = "si"
    NO = "no"


@dataclass
class Mir:
    descripcion: str
    solucionado: Solucionado
    archivos_adjuntos: list[Documento]
    nombre_empresa: str
    nombre_persona_empresa: str
    telefono_empresa: int
    codigo_cliente: str
    correo_cliente: str
    fecha_deteccion: date
    id: UUID = field(default_factory=uuid4)
