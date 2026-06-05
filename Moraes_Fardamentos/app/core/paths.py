from pathlib import Path
from app.core.config import BASE_DIR

DATA_DIR = BASE_DIR / 'data'
STORAGE_DIR = BASE_DIR / 'storage'
AUDIOS_DIR = STORAGE_DIR / 'audios'
IMAGES_DIR = STORAGE_DIR / 'images'
PDFS_DIR = STORAGE_DIR / 'pdfs'
EXPORTS_DIR = STORAGE_DIR / 'exports'
TEMP_DIR = STORAGE_DIR / 'temp'

from app.core.config import (
    AUDIO_DIR,
    DATA_DIR,
    EXPORT_DIR,
    IMAGE_DIR,
    PDF_DIR,
    STORAGE_DIR,
    TEMP_DIR,
)


def ensure_directories() -> None:
    directories = [
        DATA_DIR,
        STORAGE_DIR,
        AUDIO_DIR,
        IMAGE_DIR,
        PDF_DIR,
        EXPORT_DIR,
        TEMP_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)