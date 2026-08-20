from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class BackupInfoModel:
    """
    Informações de um backup encontrado.
    """

    system_name: str
    version: str
    database: str

    backup_type: str
    created_at: datetime

    has_data: bool
    has_orders: bool
    has_artes: bool
    has_config: bool