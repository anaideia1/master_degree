import datetime
import os
from typing import Annotated, Dict, Optional
from fastapi import (
    APIRouter, Depends, File as _File,
    UploadFile, BackgroundTasks, HTTPException,
    Request, Query
)

from fastapi.responses import Response

# from src.image_animation_app.settings import ALLOWED_TYPES, readable_allowed_types
from src.image_animation_app.schemas import (
    ImageSchema, ImageSequenceSchema, ImageSequenceLinksSchema,
    ErrorMessageSchema
)
from src.image_animation_app.models import Image, ImageSequence
from src.image_animation_app.utils import (
    check_mis_token, get_permission_data_from_str, valid_content_length,
)
from src.auth.models import User
from src.image_animation_app.responses import FileResponseOr404, DownloadResponseOr404


responses = {
    404: {"model": ErrorMessageSchema},
    403: {"model": ErrorMessageSchema},
    401: {"model": ErrorMessageSchema}
}
router = APIRouter(
    responses=responses,
    dependencies=[Depends(check_mis_token)]
)


@router.post('/', response_model=ImageSequenceSchema, status_code=201, tags=['Image sequence'])
async def create(
        background_tasks: BackgroundTasks,
        user: User,
        file: Annotated[UploadFile, _File()],
        file_size: int = Depends(valid_content_length),
):
    """
    Create new file and set given permissions on it.
    """
    # if file.content_type not in ALLOWED_TYPES:
    #     raise HTTPException(
    #         status_code=415,
    #         detail=f"File of this media type is not allowed to upload. "
    #                f"List of allowed types: {readable_allowed_types}"
    #     )
    file = await ImageSequence.create_file(file, user, background_tasks)

    return file


@router.get('/{sequence_pk}/', response_model=ImageSequenceLinksSchema, tags=['Image sequence'])
async def retrieve(
        sequence_pk: int,
        request: Request,
        user: User,
):
    """
    Return general data and  support links on file by id if you are allowed
    to see this information.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    netloc = request.url.netloc
    view_link = f'http://{netloc}/images/{sequence_pk}/view/'
    download_link = f'http://{netloc}/images/{sequence_pk}/download/'
    return {
        **sequence.dict(),
        'view_link': view_link,
        'download_link': download_link
    }


@router.patch('/{sequence_pk}/', response_model=ImageSequenceSchema, tags=['Image sequence'])
async def update(
        sequence_pk: int,
        user: User,
        archived: bool = Query(...),
):
    """
    Update archived status of file by id if you are allowed to do that.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    return await sequence.update(
        updated=datetime.datetime.now(),
        archived=archived,
    )


@router.delete('/{sequence_pk}/', status_code=204, tags=['Image sequence'])
async def delete(
        sequence_pk: int,
        user: User,
):
    """
    Delete one of files by id if you are allowed to do that.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    try:
        await sequence.delete()
        os.remove(sequence.file_name)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return Response(status_code=204)


@router.get('/{sequence_pk}/generate/', response_model=ImageSequenceSchema, tags=['Image sequence'])
async def generate_movie(
        sequence_pk: int,
        length: Optional[int],
        user: User,
):
    """
    Delete one of files by id if you are allowed to do that.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    await sequence.generate_sequence(length)

    return Response(status_code=204)


@router.get('/{sequence_pk}/view/', response_class=FileResponseOr404, tags=['Image sequence'])
async def view(
        sequence_pk: int,
        user: User,
):
    """
    Allow you to view file.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    return sequence.file_name


@router.get('/{sequence_pk}/download/', tags=['Image sequence'])
async def download(
        sequence_pk: int,
        permission_data: Annotated[
            Dict[str, str], Depends(get_permission_data_from_str)
        ],
):
    """
    Allow you to download file.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(permission_data)

    return DownloadResponseOr404(
        sequence.file_name,
        filename=sequence.file_name.split('/')[-1]
    )


@router.get('/{sequence_pk}/image/{order}', response_model=ImageSchema, tags=['Image'])
async def retrieve(
        sequence_pk: int,
        order: int,
        user: User,
):
    """
    Return general data and  support links on file by id if you are allowed
    to see this information.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    return sequence.get_image_by_order_or_404(order)


@router.get('/{sequence_pk}/image/{order}/view/', response_class=FileResponseOr404, tags=['Image'])
async def view(
        sequence_pk: int,
        order: int,
        user: User,
):
    """
    Allow you to view image.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    image = sequence.get_image_by_order_or_404(order)

    return image.name


@router.get('/{sequence_pk}/image/{order}/download/', tags=['Image'])
async def download(
        sequence_pk: int,
        order: int,
        user: User,
):
    """
    Allow you to download image.
    """
    sequence = await ImageSequence.get_sequence_or_404_by_id(sequence_pk)
    await sequence.check_permission_or_403(user)

    image = sequence.get_image_by_order_or_404(order)

    return DownloadResponseOr404(
        image.name,
        filename=image.name.split('/')[-1]
    )
