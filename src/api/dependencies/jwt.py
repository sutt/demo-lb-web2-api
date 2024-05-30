from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import ExpiredSignatureError, JWTError

from ..exceptions.http import UnauthorizedException
from ..schemas.jwt import AccessTokenPayloadSchema
from ..services.jwt import JWTService


def get_jwt_token(authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())] = None) -> str:
    if not authorization:
        msg = "Authorization token not found."
        raise UnauthorizedException(msg)

    try:
        return authorization.credentials
    except IndexError:
        raise UnauthorizedException("Invalid token format. The proper format is 'Bearer {your_token}'.")


def get_jwt_payload(token: Annotated[str, Depends(get_jwt_token)]) -> AccessTokenPayloadSchema:
    try:
        return JWTService.parse_access_token(token)
    except ExpiredSignatureError:
        raise UnauthorizedException("Token is expired.")
    except JWTError:
        raise UnauthorizedException("Token is invalid.")
