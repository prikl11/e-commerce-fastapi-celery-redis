from fastapi import APIRouter, Request, HTTPException, status
import stripe
from starlette.concurrency import run_in_threadpool

from app.dependencies import OrderServiceDep
from app.core import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    service: OrderServiceDep,
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = await run_in_threadpool(
            stripe.Webhook.construct_event, 
            payload, sig_header, settings.stripe_webhook_secret,
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = int(session["metadata"]["order_id"])
        await service.handle_payment_success(order_id=order_id)

    return {"status": "ok"}