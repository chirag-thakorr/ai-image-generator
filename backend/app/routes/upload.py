from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import os
import json
from PIL import Image

from app.services.caption_service import caption_service

router = APIRouter()


@router.post("/upload-images")
async def upload_images(
    user_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    upload_dir = f"data/uploads/{user_id}"
    os.makedirs(upload_dir, exist_ok=True)

    saved_files = []

    # Minimum validation
    if len(files) < 3:
        return {
            "error": "Minimum 3 images required for training"
        }

    metadata_file = os.path.join(upload_dir, "metadata.jsonl")

    # Existing metadata tracking
    existing_images = set()

    if os.path.exists(metadata_file):
        with open(metadata_file, "r", encoding="utf-8") as meta_file:
            for line in meta_file:
                try:
                    data = json.loads(line)
                    existing_images.add(data["image"])
                except:
                    pass

    for file in files:

        # File type validation
        if not file.content_type.startswith("image/"):
            continue

        # Duplicate check
        if file.filename in existing_images:
            continue

        file_path = os.path.join(upload_dir, file.filename)

        # Save image
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Corrupt image validation
        try:
            img = Image.open(file_path)
            img.verify()
        except Exception:
            os.remove(file_path)
            continue

        # Generate caption
        caption = caption_service.generate_caption(file_path)

        # Save metadata
        metadata = {
            "image": file.filename,
            "caption": caption
        }

        with open(metadata_file, "a", encoding="utf-8") as meta_file:
            meta_file.write(json.dumps(metadata) + "\n")

        saved_files.append(metadata)

    return {
        "message": "Files uploaded successfully",
        "files": saved_files
    }