from planify.core.interfaces.dal.project import ProjectByIdResolver, ProjectCreator, ProjectEditor, ProjectRemover
from planify.core.interfaces.dal.workspace_member import IsWorkspaceMemberResolver
from planify.core.models import dto
from planify.core.services.workspace_member import is_members
from planify.core.utils.exceptions import ProjectNotFound


async def get_project(project_id: int, workspace_id: int, dao: ProjectByIdResolver) -> dto.Project:
    project = await dao.get_by_id(project_id)
    if project.workspace_id != workspace_id:
        raise ProjectNotFound

    return project


async def create_project(project: dto.Project, dao: ProjectCreator) -> dto.Project:
    created_project = await dao.create(project)
    await dao.commit()
    return created_project


async def edit_project(
    project: dto.Project,
    project_dao: ProjectEditor,
    workspace_member_dao: IsWorkspaceMemberResolver,
) -> dto.Project:
    if not await project_dao.is_project_exists(project.id, project.workspace_id):
        raise ProjectNotFound

    await is_members([project.author_id, project.manager_id], project.workspace_id, workspace_member_dao)

    edited_project = await project_dao.update(project)
    await project_dao.commit()
    return edited_project


async def remove_project(project_id: int, workspace_id: int, project_dao: ProjectRemover) -> None:
    if not await project_dao.is_project_exists(project_id, workspace_id):
        raise ProjectNotFound

    await project_dao.remove(project_id)
    await project_dao.commit()
    return None
