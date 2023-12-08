from fastapi import HTTPException

from starlette.responses import FileResponse as DownloadResponse
from fastapi.responses import FileResponse


class FileResponseOr404(FileResponse):
    async def __call__(self, *args, **kwargs):
        try:
            await super(FileResponseOr404, self).__call__(*args, **kwargs)
        except RuntimeError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )


class DownloadResponseOr404(DownloadResponse):
    async def __call__(self, *args, **kwargs):
        try:
            await super(DownloadResponseOr404, self).__call__(*args, **kwargs)
        except RuntimeError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )
