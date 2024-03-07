from datetime import datetime, timedelta, timezone

from jose import jwt

from schemas.images import ImageSchema, ImageAddSchema
from schemas.users import UserSchema
from repositories.unitofwork import IUnitOfWork


class ImagesService:
    @staticmethod
    async def get_accessed_image_by_id(
            uow: IUnitOfWork, user_id: int, image_id: int,
    ) -> ImageSchema:
        image = await uow.images.get_by_id(_id=image_id)
        if not image:
            raise 404
        elif image.user_id != user_id:
            raise 403
        else:
            return image

    @staticmethod
    async def get_all_images(
            uow: IUnitOfWork, user: UserSchema,
    ) -> list[ImageSchema]:
        filters = {'user_id': user.id}
        return await uow.images.list(filters)

    async def get_image_by_id(
            self, uow: IUnitOfWork, user: UserSchema, image_id: int,
    ) -> ImageSchema:
        return await self.get_accessed_image_by_id(
            uow=uow, user_id=user.id, image_id=image_id,
        )

    @staticmethod
    async def create_image(
            uow: IUnitOfWork, user: UserSchema, image: ImageAddSchema
    ) -> int:
        image['user_id'] = user.id
        return await uow.images.add(data=image)

    async def update_image_by_id(
            self, uow: IUnitOfWork,
            user: UserSchema,
            image_id: int,
            image: ImageAddSchema,
    ) -> int:
        await self.get_accessed_image_by_id(
            uow=uow, user_id=user.id, image_id=image_id,
        )
        return await uow.images.update(_id=image_id, data=image)

    async def delete_image_by_id(
            self, uow: IUnitOfWork, user: UserSchema, image_id: int,
    ) -> None:
        await self.get_accessed_image_by_id(
            uow=uow, user_id=user.id, image_id=image_id,
        )
        return await uow.images.delete(
            _id=image_id
        )


