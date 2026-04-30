import os

MODEL_CACHE_DIR = "E:/AI_MODELS"
HUB_CACHE_DIR = f"{MODEL_CACHE_DIR}/hub"

os.environ["HF_HOME"] = MODEL_CACHE_DIR
os.environ["HF_HUB_CACHE"] = HUB_CACHE_DIR
os.environ["TRANSFORMERS_CACHE"] = f"{MODEL_CACHE_DIR}/transformers"

os.makedirs(HUB_CACHE_DIR, exist_ok=True)