from app.repositories import UserRepository
from app.database import UserRole, User, UserCreate, UserUpdate
from app.exceptions import (
    EmailAlreadyExists,
    PhoneAlreadyExists,
    UserNotFound,
    InvalidCredentials
)
from app.core import hash_password, verify_password


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo


    async def get_all_users(
            self,
            skip: int = 0,
            limit: int = 20,
    ) -> list[User]:
        return await self.repo.get_all(skip=skip, limit=limit)


    async def get_users_by_role(
            self,
            role: UserRole,
            skip: int = 0,
            limit: int = 20,
    ) -> list[User]:
        return await self.repo.get_by_role(role, skip, limit)


    async def get_user(self, user_id: int) -> User | None:
        user = await self.repo.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFound()
        return user


    async def get_user_by_email(self, email: str) -> User:
        user = await self.repo.get_by_email(email)
        if user is None:
            raise UserNotFound()
        return user


    async def get_user_by_phone(self, phone: str) -> User:
        user = await self.repo.get_by_phone(phone)
        if user is None:
            raise UserNotFound()
        return user

    async def register(self, data: UserCreate) -> User:
        if await self.repo.email_exists(data.email):
            raise EmailAlreadyExists()
        if data.phone and await self.repo.phone_exists(data.phone):
            raise PhoneAlreadyExists()

        user_data = data.model_dump()
        user_data["hashed_password"] = hash_password(user_data.pop("password"))

        user = User(**user_data)
        user = await self.repo.create(data=user)
        return user


    async def authenticate(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email=email)
        if user is None or not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise InvalidCredentials()
        return user


    async def update_user(
            self,
            user_id: int,
            data: UserUpdate,
    ) -> User:
        user = await self.get_user(user_id=user_id)

        user_data = data.model_dump(exclude_unset=True)

        if data.password is not None:
            user_data["hashed_password"] = hash_password(user_data.pop("password"))
        if data.email is not None and await self.repo.email_exists(data.email):
            raise EmailAlreadyExists()
        if data.phone is not None and await self.repo.phone_exists(data.phone):
            raise PhoneAlreadyExists()

        for key, value in user_data.items():
            setattr(user, key, value)

        user = await self.repo.update(data=user)
        return user


    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id=user_id)
        await self.repo.delete(data=user)


    async def change_user_role(
            self,
            user_id: int,
            role: UserRole,
    ):
        user = await self.get_user(user_id=user_id)
        return await self.repo.change_role(user=user, role=role)