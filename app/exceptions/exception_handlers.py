from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import NotFoundError, ConflictError, ValidationError


def register_exception_handlers(app):

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    