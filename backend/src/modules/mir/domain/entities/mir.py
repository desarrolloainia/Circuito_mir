from dataclasses import dataclass, field
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
    id: UUID = field(default_factory=uuid4)
