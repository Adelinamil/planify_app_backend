from fastapi import FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from .utils.exception_handlers import setup as setup_exception_handlers
from .v1 import routes


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(routes.setup())
    setup_exception_handlers(app)

    # middlewares
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")  # type: ignore
    return app
