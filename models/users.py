import datetime

from typing import List, Optional
from sqlalchemy import func, FetchedValue
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.session import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    updated: Mapped[datetime.datetime] = mapped_column(
        server_default=FetchedValue(), server_onupdate=FetchedValue()
    )

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]

    is_active: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    image_sequences: Mapped[List['ImageSequence']] = relationship(
        back_populates="user"
    )
    images: Mapped[List['Image']] = relationship(
        back_populates="user"
    )
