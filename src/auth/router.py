from datetime import datetime, timedelta
from typing import Annotated

from fastapi import (
    APIRouter, Depends, HTTPException, status
)
from fastapi.security import OAuth2PasswordRequestForm

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.schemas import Token, UserSchema
from src.auth.utils import (
    authenticate_user, create_access_token, get_current_active_user,
)

router = APIRouter()


@router.post("/token", response_model=Token, tags=['User'])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/test-user-create", response_model=UserSchema, tags=['User'])
async def test_user_create(
    username: str
):
    from src.auth.models import User
    from src.auth.utils import get_password_hash
    user = await User.objects.create(
        created=datetime.now(),
        updated=datetime.now(),
        username=username,
        password=get_password_hash(username),
        email=username,
        first_name=username,
        last_name=username,
    )
    return user


@router.get("/users/me/", response_model=UserSchema, tags=['User'])
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    return current_user
