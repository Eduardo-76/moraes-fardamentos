from datetime import datetime
from pathlib import Path
import json
import zipfile

from app.core.system_paths import SystemPaths
from app.models.backup_result_model import BackupResult
from app.models.backup_info_model import BackupInfoModel

class BackupError(Exception):
    """Erro durante a criação do backup."""

class BackupService:

    def create_backup(self) -> BackupResult:
        """
        Cria um backup completo do sistema.
        """

        SystemPaths.BACKUPS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        backup_path = (
            SystemPaths.BACKUPS_DIR /
            self._backup_filename()
        )

        total_files = 0

        try:

            with zipfile.ZipFile(
                backup_path,
                mode="w",
                compression=zipfile.ZIP_DEFLATED
            ) as zip_file:

                # Adiciona todas as pastas do sistema
                for directory in self._backup_sources():

                    total_files += self._zip_directory(
                        zip_file,
                        directory
                    )

                # Adiciona informações do backup
                zip_file.writestr(
                    "backup_info.json",
                    json.dumps(
                        self._create_backup_info(),
                        indent=4,
                        ensure_ascii=False
                    )
                )

            total_size = backup_path.stat().st_size

            return BackupResult(
                success=True,
                backup_path=backup_path,
                total_files=total_files,
                total_size=total_size
            )

        except Exception as exc:
            raise BackupError(
                "Não foi possível criar o backup."
            ) from exc

    def restore_backup(
        self,
        backup_file: Path
    ) -> None:
        """
        Restaura um backup previamente criado.
        """

        if not backup_file.exists():
            raise BackupError(
                "Arquivo de backup não encontrado."
            )

        with zipfile.ZipFile(
            backup_file,
            "r"
        ) as zip_file:

            zip_file.extractall(
                SystemPaths.PROJECT_ROOT
            )
    # ------------------------------------------------------------------

    def _backup_sources(self) -> list[Path]:
        """
        Retorna todas as pastas que fazem parte do backup.
        """

        return [
            SystemPaths.DATA_DIR,
            SystemPaths.PEDIDOS_DIR,
            SystemPaths.ARTES_DIR,
            SystemPaths.CONFIG_DIR,
        ]

    def _backup_filename(self) -> str:
        """
        Gera um nome único para o backup.
        """

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        return f"backup_{timestamp}.zip"

    def _create_backup_info(self) -> dict:
        """
        Informações inseridas dentro do ZIP.
        """

        return {

            "system": {

                "name": "Moraes Fardamentos",

                "version": "1.0.0",

                "database": "SQLite"
            },

            "backup": {

                "type": "full",

                "created_at": datetime.now().isoformat()
            },

            "contents": {

                "data": SystemPaths.DATA_DIR.exists(),

                "pedidos": SystemPaths.PEDIDOS_DIR.exists(),

                "artes": SystemPaths.ARTES_DIR.exists(),

                "config": SystemPaths.CONFIG_DIR.exists()
            }
        }

    def _zip_directory(
        self,
        zip_file: zipfile.ZipFile,
        directory: Path
    ) -> int:
        """
        Adiciona todos os arquivos de uma pasta ao ZIP.
        """

        if not directory.exists():
            return 0

        files = 0

        for file in directory.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix == ".pyc":
                continue

            if "__pycache__" in file.parts:
                continue

            if file.name in {
                "Thumbs.db",
                "desktop.ini"
            }:
                continue

            zip_file.write(
                file,
                arcname=file.relative_to(
                    SystemPaths.PROJECT_ROOT
                )
            )

            files += 1

        return files

    def _load_backup_json(
        self,
        zip_file: zipfile.ZipFile
    ) -> dict:
        """
        Lê o backup_info.json de dentro do ZIP.
        """

        with zip_file.open("backup_info.json") as file:

            return json.load(file)   

    def read_backup_info(
        self,
        backup_file: Path
    ) -> BackupInfoModel:
        """
        Lê as informações de um backup.
        """

        with zipfile.ZipFile(
            backup_file,
            "r"
        ) as zip_file:

            info = self._load_backup_json(
                zip_file
            )

        return BackupInfoModel(

            system_name=info["system"]["name"],

            version=info["system"]["version"],

            database=info["system"]["database"],

            backup_type=info["backup"]["type"],

            created_at=datetime.fromisoformat(
                info["backup"]["created_at"]
            ),

            has_data=info["contents"]["data"],

            has_orders=info["contents"]["pedidos"],

            has_artes=info["contents"]["artes"],

            has_config=info["contents"]["config"],
        )

    def validate_backup(
        self,
        backup_file: Path
    ) -> bool:
        """
        Verifica se o arquivo é um backup válido.
        """

        try:

            self.read_backup_info(
                backup_file
            )

            return True

        except Exception:

            return False


if __name__ == "__main__":

    service = BackupService()

    service.restore_backup(
        Path(
            r"backups\backup_2026-07-23_14-35-15.zip"
        )
    )

    print("Backup restaurado com sucesso!")