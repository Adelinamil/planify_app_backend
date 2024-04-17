import asyncio
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig

from planify import ConfigLoader


@pytest.fixture(scope="session")
def config_loader() -> ConfigLoader:
    return ConfigLoader(prefix="TEST_")


@pytest.fixture(scope="session")
def path() -> Path:
    path = Path(__file__).parent
    return path


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(path: Path, config_loader: ConfigLoader):
    alembic_config = AlembicConfig(str(path.parent / "alembic.ini"))
    alembic_config.set_main_option(
        "script_location", str(path.parent / "planify" / "infrastructure" / "db" / "migrations")
    )

    db_config = config_loader.db_config
    alembic_config.set_main_option(
        "sqlalchemy.url", db_config.connect.url.render_as_string(hide_password=False).replace("asyncpg", "psycopg2")
    )
    upgrade(alembic_config, "head")
