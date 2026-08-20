from pathlib import Path


class SystemPaths:

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DATA_DIR = PROJECT_ROOT / "data"

    PEDIDOS_DIR = PROJECT_ROOT / "pedidos"

    ARTES_DIR = PROJECT_ROOT / "artes"

    CONFIG_DIR = PROJECT_ROOT / "config"

    BACKUPS_DIR = PROJECT_ROOT / "backups"