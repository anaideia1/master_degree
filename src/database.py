import sqlalchemy
import databases
import ormar

from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./image_animation_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

metadata = sqlalchemy.MetaData()
database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
