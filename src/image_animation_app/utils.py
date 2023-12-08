import json
import os
from typing import Annotated
from fastapi import HTTPException, Query, Header

from dotenv import load_dotenv

from src.config import MAX_FILE_SIZE_MB

load_dotenv()


async def check_mis_token(mis_token: Annotated[str, Header()]):
    security_tokens = os.getenv('SECURITY_TOKENS').split(', ')
    if mis_token not in security_tokens:
        raise HTTPException(
            status_code=401,
            detail="MIS token is wrong."
        )


async def get_permission_data_from_str(
        permission_data_str: Annotated[str, Query(
            description="Dumped to string dictionary with key-value pairs,"
                        " which represents file access condition.",
            example='{"organization": "80a9e15b-b71b-4caf-8f2e-ff247e8a5677", '
                    '"doctor": "19dc3ed7-2169-45d8-8fa3-d918c6839bf9"}'
        )]
):
    try:
        json_data = json.loads(permission_data_str)
        if not json_data or isinstance(json_data, int):
            raise TypeError
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail="Permission data can't be serialized."
        )
    return json_data


async def valid_content_length(content_length: int = Header(...)):
    if content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Max upload size is {MAX_FILE_SIZE_MB}MB."
        )
    return content_length
