from datetime import datetime, timedelta, timezone

from jose import jwt

from schemas.images import ImageSequenceSchema, ImageSequenceAddSchema
from schemas.users import UserSchema
from repositories.unitofwork import IUnitOfWork


class ImagesSequenceService:
    @staticmethod
    async def get_accessed_image_sequence_by_id(
            uow: IUnitOfWork, user_id: int, image_sequence_id: int,
    ) -> ImageSequenceSchema:
        image_sequence = await uow.image_sequences.get_by_id(
            _id=image_sequence_id
        )
        if not image_sequence:
            raise 404
        elif image_sequence.user_id != user_id:
            raise 403
        else:
            return image_sequence

    @staticmethod
    async def get_all_image_sequences(
            uow: IUnitOfWork, user: UserSchema,
    ) -> list[ImageSequenceSchema]:
        filters = {'user_id': user.id}
        return await uow.image_sequences.list(filters)

    async def get_image_sequence_by_id(
            self, uow: IUnitOfWork, user: UserSchema, image_sequence_id: int,
    ) -> ImageSequenceSchema:
        return await self.get_accessed_image_sequence_by_id(
            uow=uow, user_id=user.id, image_sequence_id=image_sequence_id,
        )

    @staticmethod
    async def create_image_sequence(
            uow: IUnitOfWork,
            user: UserSchema,
            image_sequence: ImageSequenceAddSchema,
    ) -> int:
        image_sequence['user_id'] = user.id
        return await uow.image_sequences.add(data=image_sequence)

    async def update_image_sequence_by_id(
            self, uow: IUnitOfWork,
            user: UserSchema,
            image_sequence_id: int,
            image_sequence: ImageSequenceAddSchema,
    ) -> int:
        await self.get_accessed_image_sequence_by_id(
            uow=uow, user_id=user.id, image_sequence_id=image_sequence_id,
        )
        return await uow.image_sequences.update(
            _id=image_sequence_id, data=image_sequence
        )

    async def delete_image_sequence_by_id(
            self, uow: IUnitOfWork, user: UserSchema, image_sequence_id: int,
    ) -> None:
        await self.get_accessed_image_sequence_by_id(
            uow=uow, user_id=user.id, image_sequence_id=image_sequence_id,
        )
        return await uow.image_sequences.delete(
            _id=image_sequence_id
        )


