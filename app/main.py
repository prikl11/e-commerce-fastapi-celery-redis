from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.routers import (
    categories_router,
    products_router,
    variant_router,
    users_router,
    auth_router,
    carts_router,
    discounts_router,
    addresses_router,
    orders_router,
    payment_router,
)


app = FastAPI(title="E-Commerce API")


register_exception_handlers(app)

app.include_router(router=auth_router)
app.include_router(router=users_router)
app.include_router(router=addresses_router)
app.include_router(router=categories_router)
app.include_router(router=products_router)
app.include_router(router=variant_router)
app.include_router(router=discounts_router)
app.include_router(router=carts_router)
app.include_router(router=orders_router)
app.include_router(router=payment_router)


@app.get("/check")
async def check():
    return {"message": "OK"}