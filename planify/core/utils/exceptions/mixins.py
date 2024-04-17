class BadRequestMixin:
    status_code = 400


class UnauthorizedMixin:
    status_code = 401


class ForbiddenMixin:
    status_code = 403


class NotFoundMixin:
    status_code = 404


class ConflictMixin:
    status_code = 409
