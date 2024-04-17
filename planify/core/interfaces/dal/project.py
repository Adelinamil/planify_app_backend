from typing import Protocol

from planify.core.interfaces.dal.base import Committer
from planify.core.models import dto


class ProjectByIdResolver(Protocol):
    async def get_by_id(self, id_: int) -> dto.Project:
        raise NotImplementedError


class ProjectCreator(Committer, Protocol):
    async def create(self, project_dto: dto.Project) -> dto.Project:
        raise NotImplementedError


class IsProjectExistsResolver(Committer, Protocol):
    async def is_project_exists(self, project_id: int, workspace_id: int) -> bool:
        raise NotImplementedError


class ProjectEditor(IsProjectExistsResolver, Committer, Protocol):
    async def update(self, project_dto: dto.Project) -> dto.Project:
        raise NotImplementedError


class ProjectRemover(IsProjectExistsResolver, Committer, Protocol):
    async def remove(self, project_id: int):
        raise NotImplementedError
