from sqlalchemy import select, update
from pydantic import BaseModel

from models.images import Image, ImageSequence
from repositories.base import SQLAlchemyRepository
from schemas.images import ImageSchema, ImageSequenceSchema


class ImagesRepository(SQLAlchemyRepository):
    model = Image
    schema = ImageSchema

    async def get_all_images(
            self, user_id: int | None = None,
    ) -> list[ImageSchema]:
        filters = {'user_id': user_id}
        return await self.list(filters)

    async def update_by_id_for_user(
            self, _id: int, user_id: int, data: dict
    ) -> int:
        stmt = update(self.model).values(**data).filter_by(
            id=_id, user_id=user_id
        ).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()


class ImageSequencesRepository(SQLAlchemyRepository):
    model = ImageSequence
    schema = ImageSequenceSchema
