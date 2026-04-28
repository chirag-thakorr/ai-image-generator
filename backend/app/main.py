from fastapi import FastAPI
from pydantic import BaseModel
from app.services.image_generator import generator
from app.routes import upload


app = FastAPI()
app.include_router(upload.router)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "AI Image Generator API Running 🚀"}

@app.post("/generate")
def generate_image(data: PromptRequest):
    image_path = generator.generate(data.prompt)

    return {
        "prompt": data.prompt,
        "image_path": image_path
    }