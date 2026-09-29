from datetime import datetime
from pathlib import Path
import json
import shutil
import zipfile

from app.core.paths import (
    APP_DIR,
    DATA_DIR,
    BACKUPS_DIR,
    STORAGE_DIR,
    ARTWORK_DIR,
)
from app.models.backup_result_model import BackupResult
from app.models.backup_info_model import BackupInfoModel


class BackupError(Exception):
    """Erro durante a criação ou restauração do backup."""


class BackupService:

    def create_backup(self) -> BackupResult:
        """Cria um backup completo dos dados reais da aplicação."""
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

        backup_path = BACKUPS_DIR / self._backup_filename()
        total_files = 0

        try:
            with zipfile.ZipFile(
                backup_path,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
            ) as zip_file:
                total_files += self._zip_directory(zip_file, DATA_DIR)
                total_files += self._zip_directory(zip_file, STORAGE_DIR)

                zip_file.writestr(
                    "backup_info.json",
                    json.dumps(
                        self._create_backup_info(),
                        indent=4,
                        ensure_ascii=False,
                    ),
                )

            total_size = backup_path.stat().st_size

            return BackupResult(
                success=True,
                backup_path=backup_path,
                total_files=total_files,
                total_size=total_size,
            )

        except Exception as exc:
            if backup_path.exists():
                backup_path.unlink()
            raise BackupError(
                "Não foi possível criar o backup."
            ) from exc

    def restore_backup(self, backup_file: Path) -> None:
        """Restaura dados e arquivos de um backup válido."""
        if not backup_file.exists():
            raise BackupError("Arquivo de backup não encontrado.")

        if not self.validate_backup(backup_file):
            raise BackupError("O arquivo selecionado não é um backup válido do sistema.")

        with zipfile.ZipFile(backup_file, "r") as zip_file:
            self._validate_members(zip_file)

            # Mantém a pasta de backups para que o próprio arquivo usado
            # na restauração continue disponível.
            self._clear_directory(DATA_DIR, preserve=BACKUPS_DIR)
            self._clear_directory(STORAGE_DIR)

            for member in zip_file.infolist():
                if member.filename == "backup_info.json":
                    continue
                zip_file.extract(member, APP_DIR)

    def _backup_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"backup_{timestamp}.zip"

    def _backup_sources(self) -> list[Path]:
        return [DATA_DIR, STORAGE_DIR]

    def _create_backup_info(self) -> dict:
        return {
            "system": {
                "name": "Moraes Fardamentos",
                "version": "1.0.0",
                "database": "SQLite",
            },
            "backup": {
                "type": "full",
                "created_at": datetime.now().isoformat(),
            },
            "contents": {
                "data": DATA_DIR.exists(),
                "storage": STORAGE_DIR.exists(),
                "artes": ARTWORK_DIR.exists(),
            },
        }

    def _zip_directory(
        self,
        zip_file: zipfile.ZipFile,
        directory: Path,
    ) -> int:
        if not directory.exists():
            return 0

        files = 0

        for file in directory.rglob("*"):
            if not file.is_file():
                continue

            # Nunca inclui os próprios backups dentro de um novo backup.
            if BACKUPS_DIR == file or BACKUPS_DIR in file.parents:
                continue

            if file.suffix == ".pyc":
                continue

            if "__pycache__" in file.parts:
                continue

            if file.name in {"Thumbs.db", "desktop.ini"}:
                continue

            zip_file.write(
                file,
                arcname=file.relative_to(APP_DIR),
            )
            files += 1

        return files

    def _validate_members(self, zip_file: zipfile.ZipFile) -> None:
        allowed_roots = ("data/", "storage/")

        for member in zip_file.infolist():
            name = member.filename.replace("\\", "/")

            if name == "backup_info.json":
                continue

            if not name.startswith(allowed_roots):
                raise BackupError(
                    "O backup contém arquivos fora da estrutura esperada."
                )

            target = (APP_DIR / name).resolve()
            if APP_DIR.resolve() not in target.parents and target != APP_DIR.resolve():
                raise BackupError("O backup contém um caminho inválido.")

    def _clear_directory(
        self,
        directory: Path,
        preserve: Path | None = None,
    ) -> None:
        directory.mkdir(parents=True, exist_ok=True)

        for child in directory.iterdir():
            if preserve is not None and child.resolve() == preserve.resolve():
                continue

            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    def _load_backup_json(self, zip_file: zipfile.ZipFile) -> dict:
        with zip_file.open("backup_info.json") as file:
            return json.load(file)

    def read_backup_info(self, backup_file: Path) -> BackupInfoModel:
        with zipfile.ZipFile(backup_file, "r") as zip_file:
            info = self._load_backup_json(zip_file)

        contents = info.get("contents", {})

        return BackupInfoModel(
            system_name=info["system"]["name"],
            version=info["system"]["version"],
            database=info["system"]["database"],
            backup_type=info["backup"]["type"],
            created_at=datetime.fromisoformat(info["backup"]["created_at"]),
            has_data=bool(contents.get("data", False)),
            has_orders=bool(contents.get("storage", False)),
            has_artes=bool(contents.get("artes", False)),
            has_config=False,
        )

    def validate_backup(self, backup_file: Path) -> bool:
        try:
            self.read_backup_info(backup_file)
            with zipfile.ZipFile(backup_file, "r") as zip_file:
                self._validate_members(zip_file)
            return True
        except Exception:
            return False
