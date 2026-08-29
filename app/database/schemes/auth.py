from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = Field(default="Bearer")


class RefreshRequest(BaseModel):
    refresh_token: str