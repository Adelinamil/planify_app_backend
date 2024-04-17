from fastapi import FastAPI

from planify.api.config import ApiConfig
from planify.api.dependencies.auth import AuthProvider, current_user, get_auth_provider
from planify.infrastructure.di.db import DbProvider, dao_provider


def setup(app: FastAPI, db_provider: DbProvider, config: ApiConfig):
    auth_provider = AuthProvider(config.auth)

    app.dependency_overrides[dao_provider] = db_provider.get_dao
    app.dependency_overrides[current_user] = auth_provider.get_current_user
    app.dependency_overrides[get_auth_provider] = lambda: auth_provider
