import os
import torch
from diffusers import StableDiffusionPipeline

# ================== CACHE SETTINGS ==================
MODEL_CACHE_DIR = "E:/AI_MODELS"
HUB_CACHE_DIR = f"{MODEL_CACHE_DIR}/hub"

os.environ["HF_HOME"] = MODEL_CACHE_DIR
os.environ["HF_HUB_CACHE"] = HUB_CACHE_DIR
os.environ["TRANSFORMERS_CACHE"] = f"{MODEL_CACHE_DIR}/transformers"

os.makedirs(HUB_CACHE_DIR, exist_ok=True)

# ================== MODEL CLASS ==================
class ImageGenerator:
    def __init__(self):
        self.model_id = "runwayml/stable-diffusion-v1-5"
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading model on {self.device}...")

        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            cache_dir=HUB_CACHE_DIR   # 🔥 IMPORTANT LINE
        )

        self.pipe = self.pipe.to(self.device)

    def generate(self, prompt: str):
        image = self.pipe(prompt).images[0]

        os.makedirs("outputs", exist_ok=True)

        file_path = f"outputs/{prompt.replace(' ', '_')}.png"
        image.save(file_path)

        return file_path


generator = ImageGenerator()