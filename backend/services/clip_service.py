import numpy as np
import torch
import pickle
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from pathlib import Path
from typing import List, Tuple
import hashlib
import base64

from backend.core.config import Config


class CLIPService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(Config.CLIP_MODEL).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(Config.CLIP_MODEL)
        self.model.eval()

    def generate_image_id(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()[:16]
        return f"img_{image_hash}"

    def generate_embedding(self, image_path: str) -> np.ndarray:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        embedding = image_features.cpu().numpy()[0]
        embedding = embedding / np.linalg.norm(embedding)
        return embedding

    def generate_text_embedding(self, text: str) -> np.ndarray:
        inputs = self.processor(text=text, return_tensors="pt", padding=True).to(
            self.device
        )
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        embedding = text_features.cpu().numpy()[0]
        embedding = embedding / np.linalg.norm(embedding)
        return embedding

    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        return float(np.dot(emb1, emb2))

    def save_embedding(self, embedding: np.ndarray, image_id: str) -> str:
        filepath = Config.EMBEDDING_DIR / f"{image_id}.npy"
        np.save(filepath, embedding)
        return str(filepath)

    def load_embedding(self, image_id: str) -> np.ndarray:
        filepath = Config.EMBEDDING_DIR / f"{image_id}.npy"
        return np.load(filepath)

    def get_all_embeddings(self) -> Tuple[np.ndarray, List[dict]]:
        embeddings = []
        metadata = []
        for file in Config.EMBEDDING_DIR.glob("*.npy"):
            emb = np.load(file)
            embeddings.append(emb)
            metadata.append({"image_id": file.stem, "filepath": str(file)})
        if embeddings:
            return np.array(embeddings), metadata
        return np.empty((0, 512)), []


clip_service = CLIPService()
