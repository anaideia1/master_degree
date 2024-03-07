import datetime

from pydantic import BaseModel

from schemas.users import UserSchema


# --------------------------------------------
# Main schemas for image animation application
# --------------------------------------------


class BaseImageSequenceSchema(BaseModel):
    name: str


class ImageSequenceAddSchema(BaseImageSequenceSchema):
    pass


class ImageSequenceSchema(BaseImageSequenceSchema):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    archived: bool

    user_id: int
    user: UserSchema

    class Config:
        orm_mode = True
        from_attributes = True


class BaseImageSchema(BaseModel):
    order: int
    image_sequence_id: int


class ImageAddSchema(BaseImageSchema):
    pass


class ImageSchema(BaseImageSchema):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    user_id: int
    user: UserSchema
    image_sequence: ImageSequenceSchema

    class Config:
        orm_mode = True
        from_attributes = True


# --------------------------------------------
# Some errors schemas for proper documentation
# --------------------------------------------


class ErrorMessageSchema(BaseModel):
    detail: str
