import pytest
from httpx import AsyncClient

from tests.fixtures.user import get_test_user


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_credentials: dict):
    response = await client.get("/v1/users/current", headers=auth_credentials)
    assert response.status_code == 200

    current_user = response.json()
    test_user = get_test_user()
    assert {
        "username": test_user["username"],
        "email": test_user["email"],
        "phone": test_user["phone"],
        "first_name": test_user["first_name"],
        "last_name": test_user["last_name"],
    } == {
        "username": current_user["username"],
        "email": current_user["email"],
        "phone": current_user["phone"],
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"],
    }
