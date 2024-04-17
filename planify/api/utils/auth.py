from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param

from planify.api.models.auth import JwtToken


class CustomAuthHeader(APIKeyHeader):
    def __init__(self):
        super().__init__(name="Authorization", scheme_name="Authorization Bearer", auto_error=True)

    async def __call__(self, request: Request) -> JwtToken:
        authorization = request.headers.get("Authorization", "")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return JwtToken(token=param, token_type="Bearer")


class RefreshTokenHeader(APIKeyHeader):
    def __init__(self):
        super().__init__(name="Refresh", scheme_name="Refresh Bearer", auto_error=True)

    async def __call__(self, request: Request) -> JwtToken:
        authorization = request.headers.get("Refresh", "")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh session not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return JwtToken(token=param, token_type="Bearer")
