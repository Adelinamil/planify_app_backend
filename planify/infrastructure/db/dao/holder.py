from sqlalchemy.ext.asyncio import AsyncSession

from planify.infrastructure.db.dao.rdb import (
    UserDAO,
    RefreshSessionDAO,
    WorkspaceDAO,
    WorkspaceMemberDAO,
    ProjectDAO,
    ProjectMemberDAO,
    TaskDAO,
)


class HolderDAO:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._user = UserDAO(session)
        self._refresh_session = RefreshSessionDAO(session)
        self._workspace = WorkspaceDAO(session)
        self._workspace_member = WorkspaceMemberDAO(session)
        self._project = ProjectDAO(session)
        self._project_member = ProjectMemberDAO(session)
        self._task = TaskDAO(session)

    async def commit(self):
        await self._session.commit()

    @property
    def user(self) -> UserDAO:
        return self._user

    @property
    def refresh_session(self) -> RefreshSessionDAO:
        return self._refresh_session

    @property
    def workspace(self) -> WorkspaceDAO:
        return self._workspace

    @property
    def workspace_member(self) -> WorkspaceMemberDAO:
        return self._workspace_member

    @property
    def project(self) -> ProjectDAO:
        return self._project

    @property
    def project_member(self) -> ProjectMemberDAO:
        return self._project_member

    @property
    def task(self) -> TaskDAO:
        return self._task
