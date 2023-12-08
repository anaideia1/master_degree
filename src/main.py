from fastapi import FastAPI
import sentry_sdk

from src.config import senty_dsn
from src.database import database
from src.auth.router import router as auth_router
from src.image_animation_app.router import router as image_router


sentry_sdk.init(
    dsn=senty_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(auth_router, prefix='')
app.include_router(image_router, prefix='/sequence')
