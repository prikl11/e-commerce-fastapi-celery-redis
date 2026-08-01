from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta, timezone
from jwt import PyJWTError, ExpiredSignatureError
from fastapi import HTTPException, status
import jwt

from app.core import settings
from app.exceptions import InvalidTokenError

password_hash = PasswordHash((Argon2Hasher(), ))

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire,
        "type": "access",
    })
    encoded_jwt = jwt.encode(to_encode, settings.access_secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
    to_encode.update({
        "exp": expire,
        "type": "refresh",
    })
    encoded_jwt = jwt.encode(to_encode, settings.refresh_secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.access_secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "access":
            raise InvalidTokenError()
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenError()
    except PyJWTError:
        raise InvalidTokenError()

def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.refresh_secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise InvalidTokenError()
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenError()
    except PyJWTError:
        raise InvalidTokenError()