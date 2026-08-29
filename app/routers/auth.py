from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.database import UserCreate, TokenResponse, UserResponse
from app.dependencies import UserServiceDep
from app.core import create_access_token, create_refresh_token, decode_refresh_token
from app.exceptions import InvalidTokenError, UserNotFound


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(service: UserServiceDep, user: UserCreate):
    return await service.register(data=user)

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
    response: Response,
):
    user = await service.authenticate(email=form_data.username, password=form_data.password)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60*60*24*7,
    )

    return TokenResponse(
        access_token=access_token,
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: Request, service: UserServiceDep):
    refresh_token = request.cookies.get("refresh_token")
    payload = decode_refresh_token(token=refresh_token)
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise InvalidTokenError()

    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        raise InvalidTokenError()
    
    try:    
        user = await service.get_user(user_id=user_id)
    except Exception:
        raise UserNotFound()

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"detail": "Logged out"}