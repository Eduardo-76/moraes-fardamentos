from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
APP_NAME = os.getenv('APP_NAME', 'Fardamento App')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
APP_LANGUAGE = os.getenv('APP_LANGUAGE', 'pt')

from pathlib import Path

APP_NAME = "Fardamento App"
APP_VERSION = "0.1.0"

DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
ASSETS_DIR = BASE_DIR / "assets"

DATABASE_PATH = DATA_DIR / "app.db"

AUDIO_DIR = STORAGE_DIR / "audios"
IMAGE_DIR = STORAGE_DIR / "images"
PDF_DIR = STORAGE_DIR / "pdfs"
EXPORT_DIR = STORAGE_DIR / "exports"
TEMP_DIR = STORAGE_DIR / "temp"

DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720

DEFAULT_THEME = "dark"
DEFAULT_COLOR_THEME = "blue"
DATA_DIR.mkdir(parents=True, exist_ok=True)
print("BANCO:", DATABASE_PATH.resolve())