from fastapi import APIRouter, Depends

from dependencies import UOWDep
from schemas.images import ImageSchema, ImageAddSchema, ErrorMessageSchema
from schemas.users import UserSchema
from services.users.current_user import get_current_active_user
from services.images.images import ImagesService

responses = {
    404: {"model": ErrorMessageSchema},
    403: {"model": ErrorMessageSchema},
    401: {"model": ErrorMessageSchema}
}
image_router = APIRouter(
    responses=responses,
    tags=['Image']
)


@image_router.get('/', response_model=ImageSchema)
async def get_all_images(
        uow: UOWDep,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Return all images data accessible for current user
    """
    return await ImagesService().get_all_images(
        uow=uow, user=user
    )


@image_router.post('/', response_model=ImageSchema)
async def create_image(
        uow: UOWDep,
        image: ImageAddSchema,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Create new image with provided data
    """
    return await ImagesService().create_image(uow=uow, user=user, image=image)


@image_router.get('/{image_id}', response_model=ImageSchema)
async def get_image(
        uow: UOWDep,
        image_id: int,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Return image data by id accessible for current user
    """
    return await ImagesService().get_image_by_id(
        uow=uow, user=user, image_id=image_id
    )


@image_router.put('/{image_id}', response_model=ImageSchema)
async def update_image(
        uow: UOWDep,
        image_id: int,
        image: ImageAddSchema,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Update image data by id if it's accessible for current user
    """
    return await ImagesService().update_image_by_id(
        uow=uow, user=user, image_id=image_id, image=image
    )


@image_router.delete('/{image_id}', status_code=204)
async def delete(
        uow: UOWDep,
        image_id: int,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Delete one of images by id if you are allowed to do that.
    """
    return await ImagesService().delete_image_by_id(
        uow=uow, user=user, image_id=image_id
    )
