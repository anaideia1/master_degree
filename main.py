import sentry_sdk
import uvicorn

from fastapi import FastAPI

from backend.config import senty_dsn
from routers.users import auth_router
from routers.images.image_sequences import sequence_router
from routers.images.images import image_router


sentry_sdk.init(
    dsn=senty_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI()

app.include_router(auth_router, prefix='')
app.include_router(sequence_router, prefix='/sequence')
app.include_router(image_router, prefix='/image')

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
