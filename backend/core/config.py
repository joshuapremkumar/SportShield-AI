import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"
EMBEDDING_DIR = DATA_DIR / "embeddings"
RESULTS_DIR = DATA_DIR / "results"

UPLOAD_DIR.mkdir(exist_ok=True)
EMBEDDING_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    IPINFO_API_KEY = os.getenv("IPINFO_API_KEY", "")
    CLIP_MODEL = "openai/clip-vit-base-patch32"
    FAISS_INDEX_FILE = str(EMBEDDING_DIR / "faiss.index")
    METADATA_FILE = str(EMBEDDING_DIR / "metadata.pkl")
    MAX_SEARCH_RESULTS = 10
    SIMILARITY_THRESHOLD = 0.6
