from typing import Protocol
from uuid import UUID

from modules.mir.domain.entities.mir import Mir


class MirRepository(Protocol):
    async def create_mir(self, mir: Mir) -> Mir: ...

    async def get_mir_by_id(self, mir_id: UUID) -> Mir | None: ...

    async def get_all_mir(self) -> list[Mir]: ...

    async def update_mir(self, mir: Mir) -> Mir: ...

    async def delete_mir(self, mir_id: UUID) -> None: ...


class MirPersistenceError(Exception):
    pass


class MirNoEncontradaError(MirPersistenceError):
    pass


class DocumentoNoEncontradoError(MirPersistenceError):
    pass


class DocumentoYaAsignadoError(MirPersistenceError):
    pass
