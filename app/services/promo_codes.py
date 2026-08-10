from decimal import Decimal
from datetime import datetime, timezone

from app.repositories import PromoCodeRepository
from app.database import PromoCodeCreate, PromoCodeUpdate, PromoCode
from app.exceptions import (
    PromoCodeUsageLimitExceededError,
    PromoCodeMinOrderAmountError,
    PromoCodeNotFoundError,
    PromoCodeExpiredError,
    PromoCodeValidationError,
    PromoCodeAlreadyExists
)


class PromoCodeService:

    def __init__(self, repo: PromoCodeRepository):
        self.repo = repo


    async def get_all(self, skip: int = 0, limit: int = 20) -> list[PromoCode]:
        return await self.repo.get_all(skip=skip, limit=limit)


    async def get_by_id(self, code_id: int) -> PromoCode:
        promo_code = await self.get_by_id(code_id=code_id)
        if promo_code is None:
            raise PromoCodeNotFoundError()
        return promo_code


    async def get_by_code(self, code: str) -> PromoCode:
        promo_code = await self.repo.get_by_code(code=code)
        if promo_code is None:
            raise PromoCodeNotFoundError()
        return promo_code


    async def validate_promo_code(self, code: str, cart_total: Decimal) -> PromoCode:
        promo_code = await self.get_by_code(code=code)
        now = datetime.now(timezone.utc)
        if promo_code.starts_at is not None and now < promo_code.starts_at:
            raise PromoCodeExpiredError(code=code)
        if promo_code.expires_at is not None and now > promo_code.expires_at:
            raise PromoCodeExpiredError(code=code)
        if promo_code.usage_limit is not None and promo_code.usage_count >= promo_code.usage_limit:
            raise PromoCodeUsageLimitExceededError(code=code)
        if promo_code.min_order_amount is not None and cart_total < promo_code.min_order_amount:
            raise PromoCodeMinOrderAmountError()
        return promo_code


    def calculate_discount(self, promo_code: PromoCode, cart_total: Decimal) -> Decimal:
        if promo_code.discount_type == "percent":
            return cart_total * promo_code.discount / 100
        return min(promo_code.discount, cart_total)


    async def increment_usage(self, code_id: int) -> PromoCode:
        promo_code = await self.get_by_id(code_id=code_id)
        promo_code.usage_count += 1
        await self.repo.update(promo_code)
        return promo_code


    async def create_promo_code(self, data: PromoCodeCreate) -> PromoCode:
        if await self.repo.code_exists(data.code):
            raise PromoCodeAlreadyExists(code=data.code)
        promo_code = PromoCode(**data.model_dump())
        promo_code = await self.repo.create(code=promo_code)
        return promo_code


    async def update_promo_code(
            self,
            code_id: int,
            data: PromoCodeUpdate,
    ) -> PromoCode:
        promo_code = await self.get_by_id(code_id=code_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(promo_code, key, value)
        promo_code = await self.repo.update(promo_code)
        return promo_code


    async def delete_promo_code(self, code_id: int) -> None:
        promo_code = await self.get_by_id(code_id=code_id)
        await self.repo.delete(code=promo_code)