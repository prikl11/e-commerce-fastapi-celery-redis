from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.routers import (
    categories_router
)


app = FastAPI(title="E-Commerce API")


register_exception_handlers(app)

app.include_router(router=categories_router)


@app.get("/check")
async def check():
    return {"message": "OK"}