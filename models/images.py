import datetime
from typing import List
from sqlalchemy import ForeignKey, func, FetchedValue
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.session import Base
from models.users import User


class ImageSequence(Base):
    __tablename__ = 'image_sequence'

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    updated: Mapped[datetime.datetime] = mapped_column(
        server_default=FetchedValue(), server_onupdate=FetchedValue()
    )

    name: Mapped[str]
    archived: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="image_sequences")

    images: Mapped[List['Image']] = relationship(
        back_populates="image_sequence"
    )


class Image(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    updated: Mapped[datetime.datetime] = mapped_column(
        server_default=FetchedValue(), server_onupdate=FetchedValue()
    )

    order: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="images")

    image_sequence_id: Mapped[int] = mapped_column(
        ForeignKey("image_sequence.id")
    )
    image_sequence: Mapped[ImageSequence] = relationship(
        back_populates="images"
    )
    #
    # @classmethod
    # async def create_file(
    #         cls,
    #         file: UploadFile,
    #         permission_data: Dict[str, str],
    #         background_tasks: BackgroundTasks,
    # ):
    #     def write_file(file_name, _file: UploadFile):
    #         with open(file_name, 'wb') as buffer:
    #             shutil.copyfileobj(_file.file, buffer)
    #
    #     ext = file.filename.split('.')[-1]
    #     file_name = f'media/{uuid.uuid4().hex}.{ext}'
    #     background_tasks.add_task(
    #         write_file, file_name, file
    #     )
    #
    #     return await cls.objects.create(
    #         created=datetime.datetime.now(),
    #         updated=datetime.datetime.now(),
    #         permission_data=permission_data,
    #         file_name=file_name,
    #     )





