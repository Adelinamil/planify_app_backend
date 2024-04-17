from .mixins import BadRequestMixin, UnauthorizedMixin, NotFoundMixin, ConflictMixin


class PlanifyError(BadRequestMixin, Exception):
    notify_user = "Error"


class NoUsernameFound(NotFoundMixin, PlanifyError):
    notify_user = "The requested username was not found"


class NoUserFound(NotFoundMixin, PlanifyError):
    notify_user = "The requested user was not found"


class NoRefreshSessionFound(UnauthorizedMixin, PlanifyError):
    notify_user = "Session not found"


class SessionExpired(UnauthorizedMixin, PlanifyError):
    notify_user = "Session has expired"


class InvalidRefreshSession(UnauthorizedMixin, PlanifyError):
    notify_user = "Invalid session"


class UserExists(ConflictMixin, PlanifyError):
    notify_user = "User already exists"


class NoWorkspaceFound(NotFoundMixin, PlanifyError):
    notify_user = "The requested workspace was not found"


class NoWorkspaceMemberFound(NotFoundMixin, PlanifyError):
    notify_user = "The requested workspace member was not found"


class WorkspaceMemberExists(ConflictMixin, PlanifyError):
    notify_user = "The user is already a member of the workspace"


class WorkspaceMemberCannotBeUpdated(ConflictMixin, PlanifyError):
    notify_user = "The member cannot be updated"


class ProjectNotFound(NotFoundMixin, PlanifyError):
    notify_user = "The requested project was not found"


class ProjectMemberExists(ConflictMixin, PlanifyError):
    notify_user = "The user is already a member of the project"


class TaskNotFound(NotFoundMixin, PlanifyError):
    notify_user = "The requested task was not found"
