from uuid import UUID

from pydantic import BaseModel

from planify.core.models import dto


class CreateProjectModel(BaseModel):
    name: str

    def to_dto(self, author_id: UUID, workspace_id: int) -> dto.Project:
        return dto.Project(id=None, name=self.name, author_id=author_id, workspace_id=workspace_id)


class EditProjectModel(BaseModel):
    name: str
    description: str | None = None
    author_id: UUID | None = None
    manager_id: UUID | None = None

    def to_dto(self, project_id: int, workspace_id: int) -> dto.Project:
        return dto.Project(
            id=project_id,
            name=self.name,
            workspace_id=workspace_id,
            description=self.description,
            author_id=self.author_id,
            manager_id=self.manager_id,
        )
