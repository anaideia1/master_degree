from pydantic import BaseModel


# ------------------------------------------------
# Users authentication schemas with OAuth2 and JWT
# ------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserInDB(UserSchema):
    hashed_password: str
