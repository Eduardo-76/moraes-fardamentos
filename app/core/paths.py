from pathlib import Path
import sys


def get_app_dir() -> Path:
    """
    Retorna a raiz do projeto durante o desenvolvimento
    e a pasta do executável quando empacotado.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[2]


APP_DIR = get_app_dir()

# =========================================================
# DADOS
# =========================================================

DATA_DIR = APP_DIR / "data"

BACKUPS_DIR = DATA_DIR / "backups"

# =========================================================
# STORAGE
# =========================================================

STORAGE_DIR = APP_DIR / "storage"

RECORDINGS_DIR = STORAGE_DIR / "recordings"

ARTWORK_DIR = STORAGE_DIR / "artwork"

AUDIO_DIR = STORAGE_DIR / "audios"

IMAGE_DIR = STORAGE_DIR / "images"

PDF_DIR = STORAGE_DIR / "pdfs"

EXPORT_DIR = STORAGE_DIR / "exports"

TEMP_DIR = STORAGE_DIR / "temp"

# =========================================================
# RECURSOS
# =========================================================

ASSETS_DIR = APP_DIR / "assets"

DOCS_DIR = APP_DIR / "docs"


def ensure_directories() -> None:
    directories = [
        DATA_DIR,
        BACKUPS_DIR,
        STORAGE_DIR,
        RECORDINGS_DIR,
        ARTWORK_DIR,
        AUDIO_DIR,
        IMAGE_DIR,
        PDF_DIR,
        EXPORT_DIR,
        TEMP_DIR,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )