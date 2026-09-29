from app.core.paths import (
    APP_DIR,
    DATA_DIR,
    BACKUPS_DIR,
    STORAGE_DIR,
    ARTWORK_DIR,
)


class SystemPaths:
    """Compatibilidade para os módulos administrativos antigos."""

    PROJECT_ROOT = APP_DIR
    DATA_DIR = DATA_DIR
    BACKUPS_DIR = BACKUPS_DIR

    # Mantidos como aliases para evitar quebra de imports antigos.
    PEDIDOS_DIR = STORAGE_DIR
    ARTES_DIR = ARTWORK_DIR
    CONFIG_DIR = APP_DIR / "config"
