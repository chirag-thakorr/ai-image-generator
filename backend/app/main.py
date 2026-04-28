from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "AI Image Generator API Running 🚀"}

@app.post("/generate")
def generate_image(data: PromptRequest):
    return {
        "prompt": data.prompt,
        "status": "received"
    }