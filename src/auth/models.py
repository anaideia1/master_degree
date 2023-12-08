import datetime
import ormar
import pathlib

from src.database import MainMeta

basedir = pathlib.Path(__file__).parent.parent.absolute()


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    created: datetime.datetime = ormar.DateTime()
    updated: datetime.datetime = ormar.DateTime()

    username: str = ormar.String(max_length=100, unique=True)
    password: str = ormar.String(max_length=100)

    email: str = ormar.String(max_length=100, unique=True)
    first_name: str = ormar.String(max_length=100)
    last_name: str = ormar.String(max_length=100, null=True)

    is_active: bool = ormar.Boolean(default=False)
    is_staff: bool = ormar.Boolean(default=False)
    is_superuser: bool = ormar.Boolean(default=False)

    @classmethod
    async def get_all_users(cls):
        return await cls.objects.all()

    @classmethod
    async def get_active_users(cls):
        return await cls.objects.filter(is_active=True).all()

    @classmethod
    async def get_user_or_none_by_id(cls, _id: int):
        return await cls.objects.get_or_none(id=_id)

    @classmethod
    async def get_user_or_none_by_username(cls, _username: str):
        return await cls.objects.get_or_none(
            username__contains=_username
        )
