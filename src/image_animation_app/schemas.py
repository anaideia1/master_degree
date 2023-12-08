import datetime

from pydantic import BaseModel, AnyUrl

from src.auth.schemas import UserSchema


# --------------------------------------------
# Main schemas for image animation application
# --------------------------------------------
class ProjectBaseSchema(BaseModel):
    id: int
    created: datetime.datetime
    updated: datetime.datetime


class ImageSequenceSchema(ProjectBaseSchema):
    user: UserSchema
    name: str
    archived: bool

    class Config:
        orm_mode = True


class ImageSequenceLinksSchema(ImageSequenceSchema):
    view_link: AnyUrl
    download_link: AnyUrl


class ImageSchema(ProjectBaseSchema):
    order: UserSchema
    sequence: ImageSequenceSchema

    class Config:
        orm_mode = True


# --------------------------------------------
# Some errors schemas for proper documentation
# --------------------------------------------
class ErrorMessageSchema(BaseModel):
    detail: str
