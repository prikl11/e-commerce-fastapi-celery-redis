from fastapi import Depends
from typing import Annotated

from app.dependencies import SessionDep
from app.repositories import AddressRepository
from app.services import AddressService

def get_address_repository(session: SessionDep) -> AddressRepository:
    return AddressRepository(session)

def get_address_service(repo: Annotated[AddressRepository, Depends(get_address_repository)]) -> AddressService:
    return AddressService(repo)

AddressServiceDep = Annotated[AddressService, Depends(get_address_service)]