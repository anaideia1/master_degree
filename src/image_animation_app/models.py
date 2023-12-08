import datetime
import ormar
import pathlib
import shutil
import uuid
from typing import Dict
from fastapi import UploadFile, BackgroundTasks, HTTPException

from src.database import MainMeta
from src.auth.models import User


basedir = pathlib.Path(__file__).parent.parent.absolute()


class ImageSequence(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    created: datetime.datetime = ormar.DateTime()
    updated: datetime.datetime = ormar.DateTime()

    user: User = ormar.ForeignKey(User)
    name: str = ormar.String(max_length=1000)
    archived: bool = ormar.Boolean(default=False)

    @classmethod
    async def get_all_sequences(cls):
        return await cls.objects.all()

    @classmethod
    async def get_active_sequences(cls):
        return await cls.objects.filter(archived=False).all()

    @classmethod
    async def get_sequence_or_none_by_id(cls, _id: int):
        return await cls.objects.get_or_none(
            id=_id
        )

    @classmethod
    async def get_sequence_or_404_by_id(cls, _id: int):
        file = await cls.objects.get_or_none(
            id=_id
        )
        if not file:
            raise HTTPException(status_code=404,
                                detail='Image does not exist!')
        return file

    @classmethod
    async def get_sequence_or_none_by_name(cls, name: str):
        return await cls.objects.get_or_none(
            name__contains=name
        )

    async def check_permission_or_403(self, user: User):
        pass

    async def generate_next(self):
        pass

    async def generate_sequence(self, length):
        pass

    async def get_image_by_order_or_404(self, order):
        pass


class Image(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    created: datetime.datetime = ormar.DateTime()
    updated: datetime.datetime = ormar.DateTime()

    sequence: ImageSequence = ormar.ForeignKey(ImageSequence)
    order: int = ormar.Integer()

    @classmethod
    async def get_all_images(cls):
        return await cls.objects.all()

    @classmethod
    async def get_image_or_none_by_id(cls, _id: int):
        return await cls.objects.get_or_none(
            id=_id
        )

    @classmethod
    async def get_image_or_404_by_id(cls, _id: int):
        file = await cls.objects.get_or_none(
            id=_id
        )
        if not file:
            raise HTTPException(status_code=404, detail='Image does not exist!')
        return file

    @classmethod
    async def create_file(
            cls,
            file: UploadFile,
            permission_data: Dict[str, str],
            background_tasks: BackgroundTasks,
    ):
        def write_file(file_name, _file: UploadFile):
            with open(file_name, 'wb') as buffer:
                shutil.copyfileobj(_file.file, buffer)

        ext = file.filename.split('.')[-1]
        file_name = f'media/{uuid.uuid4().hex}.{ext}'
        background_tasks.add_task(
            write_file, file_name, file
        )

        return await cls.objects.create(
            created=datetime.datetime.now(),
            updated=datetime.datetime.now(),
            permission_data=permission_data,
            file_name=file_name,
        )





