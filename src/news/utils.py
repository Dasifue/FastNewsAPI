"""
Utils
"""

import os
import aiofiles
from fastapi import UploadFile

from ..environs import MEDIA_ROOT



async def save_media(upload_file: UploadFile) -> str:
    file_path = os.path.join(MEDIA_ROOT, upload_file.filename)

    async with aiofiles.open(file=file_path, mode="wb") as file:
        await file.write(await upload_file.read())

    return file_path
