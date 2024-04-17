from fastapi import Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from planify.core.utils.exceptions import PlanifyError


async def planify_error_handler(request: Request, exc: PlanifyError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.notify_user},
    )


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "ValidationError", "detail": jsonable_encoder(exc.errors())},
    )


def setup(app: FastAPI):
    app.exception_handler(PlanifyError)(planify_error_handler)
