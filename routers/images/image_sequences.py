from fastapi import APIRouter, Depends

from dependencies import UOWDep
from schemas.images import (
    ImageSequenceSchema, ImageSequenceAddSchema, ErrorMessageSchema,
)
from schemas.users import UserSchema
from services.users.current_user import get_current_active_user
from services.images.image_sequences import ImagesSequenceService

responses = {
    404: {"model": ErrorMessageSchema},
    403: {"model": ErrorMessageSchema},
    401: {"model": ErrorMessageSchema}
}

sequence_router = APIRouter(
    responses=responses,
    tags=['Image sequence']
)


@sequence_router.get('/', response_model=ImageSequenceSchema)
async def get_all_images(
        uow: UOWDep,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Return all images data accessible for current user
    """
    return await ImagesSequenceService().get_all_image_sequences(
        uow=uow, user=user
    )


@sequence_router.post('/', response_model=ImageSequenceSchema)
async def create_image(
        uow: UOWDep,
        image_sequence: ImageSequenceAddSchema,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Create new image with provided data
    """
    return await ImagesSequenceService().create_image_sequence(
        uow=uow, user=user, image_sequence=image_sequence,
    )


@sequence_router.get('/{image_id}', response_model=ImageSequenceSchema)
async def get_image(
        uow: UOWDep,
        image_sequence_id: int,
        user: UserSchema = Depends(get_current_active_user),

):
    """
    Return image data by id accessible for current user
    """
    return await ImagesSequenceService().get_image_sequence_by_id(
        uow=uow, user=user, image_sequence_id=image_sequence_id,
    )


@sequence_router.put('/{image_id}', response_model=ImageSequenceSchema)
async def update_image(
        uow: UOWDep,
        image_sequence_id: int,
        image_sequence: ImageSequenceAddSchema,
        user: UserSchema = Depends(get_current_active_user),
):
    """
    Update image data by id if it's accessible for current user
    """
    return await ImagesSequenceService().update_image_sequence_by_id(
        uow=uow,
        user=user,
        image_sequence_id=image_sequence_id,
        image_sequence=image_sequence,
    )


@sequence_router.delete('/{image_id}', status_code=204)
async def delete(
        uow: UOWDep,
        image_sequence_id: int,
        user: UserSchema = Depends(get_current_active_user),

):
    """
    Delete one of images by id if you are allowed to do that.
    """
    return await ImagesSequenceService().delete_image_sequence_by_id(
        uow=uow, user=user, image_sequence_id=image_sequence_id
    )
