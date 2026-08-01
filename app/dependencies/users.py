from typing import Annotated
from fastapi import Depends

from app.repositories import UserRepository
from app.services import UserService
from app.dependencies import SessionDep


def get_user_repository(db: SessionDep) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]