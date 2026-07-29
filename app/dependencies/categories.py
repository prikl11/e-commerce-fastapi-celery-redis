from typing import Annotated
from fastapi import Depends

from app.repositories import CategoryRepository
from app.services import CategoryService
from app.dependencies import SessionDep


def get_category_repository(db: SessionDep) -> CategoryRepository:
    return CategoryRepository(db)


def get_category_service(repo: Annotated[CategoryRepository, Depends(get_category_repository)]) -> CategoryService:
    return CategoryService(repo)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]