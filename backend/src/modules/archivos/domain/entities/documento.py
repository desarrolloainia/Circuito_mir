from dataclasses import dataclass, field
from uuid import UUID, uuid4

from modules.archivos.domain.Enum.estado_documetno import TipoDocumento


@dataclass
class Documento:
    nombre: str
    tipo: TipoDocumento
    storage_id: str
    creado_por: UUID
    id: UUID = field(default_factory=uuid4)
