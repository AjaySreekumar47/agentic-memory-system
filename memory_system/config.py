import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MEMORY_DB_DIR = DATA_DIR / "memory_db"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

TOP_K_CANDIDATES = 5
TOP_K_RETRIEVAL = 5
LINK_EXPANSION_LIMIT = 5