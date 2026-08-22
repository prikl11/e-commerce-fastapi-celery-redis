from app.database import Address, AddressCreate, AddressUpdate
from app.repositories import AddressRepository
from app.exceptions import AddressNotFoundError


class AddressService:

    def __init__(self, repo: AddressRepository):
        self.repo = repo


    async def get_all_by_user(self, user_id: int) -> list[Address]:
        return await self.repo.get_all_by_user(user_id=user_id)


    async def get_by_id(self, address_id: int) -> Address:
        address = await self.repo.get_by_id(address_id=address_id)
        if not address_id:
            raise AddressNotFoundError()
        return address


    async def get_by_id_and_user(
            self, address_id: int, user_id: int,
    ) -> Address:
        address = await self.repo.get_by_id_and_user(address_id=address_id, user_id=user_id)
        if not address:
            raise AddressNotFoundError()
        return address


    async def create(self, data: AddressCreate) -> Address:
        address = Address(**data.model_dump())
        return await self.repo.create(data=address)


    async def update(
            self, address_id: int, data: AddressUpdate, user_id: int
    ) -> Address:
        address = await self.get_by_id_and_user(address_id=address_id, user_id=user_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(address, key, value)
        return await self.repo.update(data=address)


    async def delete(self, address_id: int, user_id: int) -> None:
        address = await self.get_by_id_and_user(address_id=address_id, user_id=user_id)
        await self.repo.delete(data=address)