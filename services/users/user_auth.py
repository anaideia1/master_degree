from datetime import datetime, timedelta, timezone

from jose import jwt

from backend.config import SECRET_KEY, ALGORITHM
from schemas.users import UserSchema, Token
from backend.config import pwd_context, ACCESS_TOKEN_EXPIRE
from repositories.unitofwork import IUnitOfWork


class UserAuthService:
    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def _create_token(
            data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def _create_access_token(self, data: dict) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
        return await self._create_token(
            data=data, expires_delta=access_token_expires
        )

    async def authenticate_user(
            self, uow: IUnitOfWork, username: str, password: str
    ) -> (UserSchema | None, Token | None):
        async with uow:
            user = await uow.users.get_by_username(username)
            if not user or not self._verify_password(
                    password, user.hashed_password
            ):
                return None, None

            access_token = Token(
                access_token=await self._create_access_token(
                    data={"sub": user.username}
                ),
                token_type='bearer'
            )
            return user, access_token
