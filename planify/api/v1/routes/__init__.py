from fastapi import APIRouter

from . import user, auth, workspace, project, task


def setup() -> APIRouter:
    router = APIRouter(prefix="/api/v1")
    router.include_router(user.setup())
    router.include_router(auth.setup())
    router.include_router(workspace.setup())
    router.include_router(project.setup())
    router.include_router(task.setup())
    return router
