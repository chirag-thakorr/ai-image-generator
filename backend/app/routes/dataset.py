from fastapi import APIRouter
import os
import json

router = APIRouter()

@router.get("/dataset/{user_id}")
async def get_dataset(user_id: str):

    upload_dir = f"data/uploads/{user_id}"
    metadata_file = os.path.join(upload_dir, "metadata.jsonl")

    if not os.path.exists(metadata_file):
        return {
            "error": "Dataset not found"
        }

    images = []

    with open(metadata_file, "r", encoding="utf-8") as meta_file:
        for line in meta_file:
            images.append(json.loads(line))

    return {
        "user_id": user_id,
        "total_images": len(images),
        "dataset_ready": len(images) >= 3,
        "images": images
    }