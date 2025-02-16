"""
Media routers
"""

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/file",
    tags=["Media"]
)

@router.get("/{file_path:path}", response_class=FileResponse)
async def get_media(file_path: str) -> FileResponse:
    file = os.path.join(file_path)
    if not os.path.isfile(file):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file)
