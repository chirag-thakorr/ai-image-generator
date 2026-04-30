from fastapi import APIRouter, UploadFile, File
from typing import List
import os
from app.services.caption_service import caption_service
import json

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
        caption = caption_service.generate_caption(file_path)

        saved_files.append({
            "filename": file.filename,
            "caption": caption
        })

        metadata = {
            "image": file.filename,
            "caption": caption
        }

        metadata_file = os.path.join(UPLOAD_DIR, "metadata.jsonl")

        with open(metadata_file, "a", encoding="utf-8") as meta_file:
            meta_file.write(json.dumps(metadata) + "\n")
        # saved_files.append(file.filename)

    return {
        "message": "Files uploaded successfully",
        "files": saved_files
    }