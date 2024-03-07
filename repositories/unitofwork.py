from abc import ABC, abstractmethod
from typing import Type

from backend.session import async_session_maker
from repositories.users import UsersRepository
from repositories.images import (
    ImagesRepository, ImageSequencesRepository
)


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    images: Type[ImagesRepository]
    image_sequences: Type[ImageSequencesRepository]

    @abstractmethod
    def __init__(self):
        """ Init method  """

    @abstractmethod
    async def __aenter__(self):
        """ Async context manager enter method  """

    @abstractmethod
    async def __aexit__(self, *args):
        """ Async context manager exit method  """

    @abstractmethod
    async def commit(self):
        """ Commit method of current unit of work  """

    @abstractmethod
    async def rollback(self):
        """ Rollback method of current unit of work  """


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.images = ImagesRepository(self.session)
        self.image_sequences = ImageSequencesRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
