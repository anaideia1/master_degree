from fastapi import HTTPException, Header

from dotenv import load_dotenv

from backend.config import MAX_FILE_SIZE_MB

load_dotenv()


async def valid_content_length(content_length: int = Header(...)):
    if content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Max upload size is {MAX_FILE_SIZE_MB}MB."
        )
    return content_length
