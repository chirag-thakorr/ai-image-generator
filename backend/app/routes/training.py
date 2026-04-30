from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import os
import json
import asyncio


router = APIRouter()

# Temporary in-memory job storage
training_jobs = {}


async def simulate_training(job_id: str):

    # Step 1
    # training_jobs[job_id]["status"] = "training"
    user_id = training_jobs[job_id]["user_id"]

    # Create LoRA output folder
    output_dir = f"models/lora/{user_id}"
    os.makedirs(output_dir, exist_ok=True)

    # Fake checkpoint file (temporary)
    checkpoint_path = os.path.join(output_dir, "adapter_config.json")

    with open(checkpoint_path, "w") as f:
        json.dump({
            "status": "trained",
            "user_id": user_id
        }, f)

    training_jobs[job_id]["status"] = "completed"
    training_jobs[job_id]["output_dir"] = output_dir

    # Simulate training time
    # await asyncio.sleep(10)

    # Step 2
    # training_jobs[job_id]["status"] = "completed"



class TrainingRequest(BaseModel):
    user_id: str


@router.post("/start-training")
async def start_training(data: TrainingRequest):

    upload_dir = f"data/uploads/{data.user_id}"
    metadata_file = os.path.join(upload_dir, "metadata.jsonl")

    # Dataset check
    if not os.path.exists(metadata_file):
        return {
            "error": "Dataset not found"
        }

    # Read dataset
    with open(metadata_file, "r", encoding="utf-8") as meta_file:
        dataset = meta_file.readlines()

    # Minimum dataset validation
    if len(dataset) < 3:
        return {
            "error": "Minimum 3 images required for training"
        }

    # Create training job
    job_id = str(uuid.uuid4())

    training_jobs[job_id] = {
        "user_id": data.user_id,
        "status": "queued",
        "images": len(dataset)
    }

    asyncio.create_task(simulate_training(job_id))

    return {
        "message": "Training job created successfully",
        "job_id": job_id,
        "status": "queued"
    }




@router.get("/training-status/{job_id}")
async def get_training_status(job_id: str):

    job = training_jobs.get(job_id)

    if not job:
        return {
            "error": "Training job not found"
        }

    return {
        "job_id": job_id,
        "status": job["status"],
        "user_id": job["user_id"],
        "images": job["images"]
    }