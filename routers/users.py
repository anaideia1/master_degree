from datetime import datetime, timedelta
from typing import Annotated

from fastapi import (
    APIRouter, Depends, HTTPException, status
)
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import UOWDep
from schemas.users import Token, UserSchema
from services.users.user_auth import UserAuthService
from services.users.current_user import get_current_active_user

auth_router = APIRouter()


@auth_router.post("/token", response_model=Token, tags=['User'])
async def login_for_access_token(
    uow: UOWDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user, access_token = await UserAuthService().authenticate_user(
        uow, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return access_token


@auth_router.post("/test-user-create", response_model=UserSchema, tags=['User'])
async def test_user_create(
    uow: UOWDep,
    username: str,
):
    user_data = dict(
        created=datetime.now(),
        updated=datetime.now(),
        username=username,
        hashed_password=UserAuthService().get_password_hash(username),
        email=username,
        first_name=username,
        last_name=username,
    )
    async with uow:
        print(await uow.users.add(user_data))
        await uow.commit()

    user_data.update({'id': 0})
    return user_data


@auth_router.get("/users/me/", response_model=UserSchema, tags=['User'])
async def read_users_me(
    current_user: Annotated[
        UserSchema, Depends(get_current_active_user)
    ]
):
    return current_user
