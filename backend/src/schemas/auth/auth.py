from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(3600, description="Срок действия токена в секундах")


class RefreshTokenRequest(BaseModel):
    refresh_token: str
