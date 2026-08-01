from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from app.dependencies import UserServiceDep
from app.core import decode_access_token
from app.database import User, UserRole
from app.exceptions import InvalidTokenError, UserNotFound, UserPermissionDenied

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], service: UserServiceDep):
    payload = decode_access_token(token=token)
    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidTokenError()

    try:
        user = await service.get_user(user_id=int(user_id))
    except UserNotFound:
        raise InvalidTokenError()

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: UserRole):
    async def dependency(current_user: CurrentUserDep) -> User:
        if current_user.role not in roles:
            raise UserPermissionDenied()
        return current_user
    return dependency
