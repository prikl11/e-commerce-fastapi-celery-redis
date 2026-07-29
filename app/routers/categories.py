from fastapi import APIRouter

from app.dependencies import CategoryServiceDep
from app.database import CategoryResponse, CategoryCreate, CategoryUpdate


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(service: CategoryServiceDep, parent_id: int | None = None):
    return await service.get_all_categories(parent_id=parent_id)

@router.get("/slug/{slug}", response_model=CategoryResponse)
async def get_category_by_slug(service: CategoryServiceDep, slug: str):
    return await service.get_category_by_slug(slug=slug)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(service: CategoryServiceDep, category_id: int):
    return await service.get_category(category_id=category_id)

@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, service: CategoryServiceDep):
    return await service.create_category(data=data)

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, data: CategoryUpdate, service: CategoryServiceDep):
    return await service.update_category(category_id=category_id, data=data)

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, service: CategoryServiceDep):
    await service.delete_category(category_id=category_id)