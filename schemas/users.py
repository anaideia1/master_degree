import datetime

from pydantic import BaseModel


# ------------------------------------------------
# Users authentication schemas with OAuth2 and JWT
# ------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class BaseUserSchema(BaseModel):
    username: str
    email: str
    last_name: str
    first_name: str


class UserAddSchema(BaseUserSchema):
    pass


class UserSchema(BaseUserSchema):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    is_active: bool = False
    is_staff: bool = False
    is_superuser: bool = False

    class Config:
        orm_mode = True
        from_attributes = True


class UserInDB(UserSchema):
    hashed_password: str
