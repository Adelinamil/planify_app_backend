from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from planify import ConfigLoader, create_app, DbProvider
from planify.api import dependencies
from tests.fixtures.user import get_test_user


@pytest.fixture(scope="session")
def app(config_loader: ConfigLoader) -> FastAPI:
    app = create_app()
    db_provider = DbProvider(config_loader.db_config)
    dependencies.setup(app, db_provider, config_loader.api_config)
    return app


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/api"  # noqa
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
async def auth_credentials(client: AsyncClient) -> dict:
    test_user = get_test_user()
    await client.post(
        "/v1/users/create",
        json=test_user,
    )
    response = await client.post(
        "/v1/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"],
            "fingerprint": test_user["fingerprint"],
        },
    )
    response_data = response.json()
    return {
        "Authorization": f"{response_data['access']['token_type']} {response_data['access']['token']}",
        "Refresh": f"{response_data['refresh']['token_type']} {response_data['refresh']['token']}",
    }
