from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import NotFoundError, ConflictError, ValidationError, AuthenticationError, PermissionDeniedError


def register_exception_handlers(app):

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})

    @app.exception_handler(AuthenticationError)
    async def authentication_error(request: Request, exc: AuthenticationError):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied(request: Request, exc: PermissionDeniedError):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)})