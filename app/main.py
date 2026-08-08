from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.routers import (
    categories_router,
    products_router,
    variant_router,
    users_router,
    auth_router,
    carts_router,
)


app = FastAPI(title="E-Commerce API")


register_exception_handlers(app)

app.include_router(router=auth_router)
app.include_router(router=users_router)
app.include_router(router=categories_router)
app.include_router(router=products_router)
app.include_router(router=variant_router)
app.include_router(router=carts_router)


@app.get("/check")
async def check():
    return {"message": "OK"}