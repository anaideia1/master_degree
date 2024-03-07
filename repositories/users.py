from models.users import User
from schemas.users import UserInDB
from repositories.base import SQLAlchemyRepository
from sqlalchemy import select


class UsersRepository(SQLAlchemyRepository):
    model = User
    schema = UserInDB

    async def get_by_username(self, username: str) -> UserInDB:
        stmt = select(self.model).filter_by(username=username)
        user = await self.session.execute(stmt)
        user = user.scalar_one()
        return self.schema.from_orm(user)
