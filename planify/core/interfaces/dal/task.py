from typing import Protocol

from planify.core.interfaces.dal.base import Committer
from planify.core.models import dto


class TaskByIdResolver(Protocol):
    async def get_by_id(self, id_: int) -> dto.Task:
        raise NotImplementedError


class IsTaskExistsResolver(Committer, Protocol):
    async def is_task_exists(self, task_id: int, workspace_id: int) -> bool:
        raise NotImplementedError


class TaskCreator(Committer, Protocol):
    async def create(self, task_dto: dto.Task) -> dto.Task:
        raise NotImplementedError


class TaskEditor(IsTaskExistsResolver, Committer, Protocol):
    async def update(self, task_dto: dto.Task) -> dto.Task:
        raise NotImplementedError


class TaskRemover(IsTaskExistsResolver, Committer, Protocol):
    async def remove(self, task_id: int):
        raise NotImplementedError
