import os

from dotenv import load_dotenv

from app.core.paths import (
    APP_DIR,
    DATA_DIR,
    STORAGE_DIR,
    ASSETS_DIR,
    AUDIO_DIR,
    IMAGE_DIR,
    PDF_DIR,
    EXPORT_DIR,
    TEMP_DIR,
)

load_dotenv()


# =========================================================
# APLICAÇÃO
# =========================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "Fardamento App"
)

APP_VERSION = "0.1.0"

APP_LANGUAGE = os.getenv(
    "APP_LANGUAGE",
    "pt"
)


# =========================================================
# IA
# =========================================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "mistral"
)


# =========================================================
# BANCO
# =========================================================

DATABASE_PATH = DATA_DIR / "app.db"


# =========================================================
# JANELA
# =========================================================

DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720


# =========================================================
# TEMA
# =========================================================

DEFAULT_THEME = "dark"
DEFAULT_COLOR_THEME = "blue"


print(
    "BANCO:",
    DATABASE_PATH.resolve()
)