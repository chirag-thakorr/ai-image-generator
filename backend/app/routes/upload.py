from fastapi import APIRouter, UploadFile, File
from typing import List
import os

router = APIRouter()

UPLOAD_DIR = "data/uploads"

@router.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    saved_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        saved_files.append(file.filename)

    return {
        "message": "Files uploaded successfully",
        "files": saved_files
    }