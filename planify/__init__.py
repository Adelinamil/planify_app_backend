from functools import partial

from fastapi import FastAPI

from planify.api import dependencies
from planify.api.main_factory import create_app
from planify.common.config_loader import ConfigLoader
from planify.infrastructure.di.db import DbProvider


async def on_shutdown(db_provider: DbProvider):
    await db_provider.shutdown()


def main() -> FastAPI:
    config_loader = ConfigLoader()
    app = create_app()
    db_provider = DbProvider(config_loader.db_config)
    dependencies.setup(app, db_provider, config_loader.api_config)

    app.add_event_handler("shutdown", partial(on_shutdown, db_provider))
    return app
