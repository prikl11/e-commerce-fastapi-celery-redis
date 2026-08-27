import stripe
from decimal import Decimal
from starlette.concurrency import run_in_threadpool

from app.core import settings


class PaymentService:

    def __init__(self):
        stripe.api_key = settings.stripe_secret_key


    async def create_payment_session(self, order_id: int, amount: Decimal):
        session = await run_in_threadpool(
            stripe.checkout.Session.create,
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Order #{order_id}",
                            },
                            "unit_amount": int(amount * 100),
                        },
                        "quantity": 1,
                    }
                ],
                success_url="http://localhost:8000/success",
                cancel_url="http://localhost:8000/cancel",
                metadata={"order_id": str(order_id)},
            )
        return session.id, session.url