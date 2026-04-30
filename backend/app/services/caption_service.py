from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from app.core.config import HUB_CACHE_DIR

class CaptionService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading BLIP model on {self.device}...")

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base",
            cache_dir=HUB_CACHE_DIR
        )

        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base",
            cache_dir=HUB_CACHE_DIR
        ).to(self.device)

    def generate_caption(self, image_path: str):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(image, return_tensors="pt").to(self.device)

        out = self.model.generate(**inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)

        return caption


caption_service = CaptionService()