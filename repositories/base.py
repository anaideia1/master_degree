from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel
from backend.session import Base


class IRepository(ABC):
    @abstractmethod
    async def list(self, **filter_by) -> list[BaseModel]:
        """
        Return filtered list of records in DTO form
        :param filter_by: Filter conditions, several criteria are linked with a logical 'and'.
        :return: list of DTOs
        """
    @abstractmethod
    async def get(self, **filter_by) -> BaseModel:
        """
        Return record in DTO form
        :param filter_by: Filter conditions, several criteria are linked with a logical 'and'.
        :return: DTO of record
        """

    @abstractmethod
    async def get_by_id(self, _id: int) -> BaseModel:
        """
        Return record in DTO form
        :param _id: record id
        :return: DTO of record
        """

    @abstractmethod
    async def add(self, data: dict) -> int:
        """
        Add new record with offered data
        :param data: data for record adding
        :return: new record id
        """

    @abstractmethod
    async def update(self, _id: int, data: dict) -> int:
        """
        Update record found by id with offered data
        :param _id: record id
        :param data: data for record updating
        :return: record id
        """

    @abstractmethod
    async def delete(self, _id: int) -> None:
        """
        Delete record found by id
        :param _id: record id
        :return:
        """


class SQLAlchemyRepository(IRepository):
    model: Base | None = None
    schema: BaseModel | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, **filter_by) -> list[BaseModel]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [self.schema.from_orm(row[0]) for row in res.all()]
        return res

    async def get(self, **filter_by) -> BaseModel:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = self.schema.from_orm(res.scalar_one())
        return res

    async def get_by_id(self, _id: int) -> BaseModel:
        stmt = select(self.model).filter_by(id=_id)
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_read_model()
        return self.schema.from_orm(res)

    async def add(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update(self, _id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=_id).returning(
            self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, _id: int) -> None:
        record = self.get_by_id(_id=_id)
        if record is not None:
            await self.session.delete(record)
