from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BackupResult:
    """
    Resultado da criação de um backup.
    """

    success: bool
    backup_path: Path
    total_files: int
    total_size: int