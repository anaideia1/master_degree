from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from backend.config import SECRET_KEY, ALGORITHM, oauth2_scheme
from dependencies import UOWDep

from schemas.users import UserSchema, TokenData


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        uow: UOWDep,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    async with uow:
        current_user = await uow.users.get_by_username(token_data.username)

    if current_user is None:
        raise credentials_exception
    return current_user


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
