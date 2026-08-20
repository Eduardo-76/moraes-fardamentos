from app.models.print_job_model import PrintJobModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

TEMPLATE_PATH = (
    BASE_DIR
    / "assets"
    / "templates"
    / "comanda_template.jpeg"
)


class PrintService:

    def __init__(self):
        pass

    def load_template(self):
        """
        Carrega o template da comanda.
        """
        pass

    def generate_preview(
        self,
        print_job: PrintJobModel
    ):
        """
        Gera uma pré-visualização da comanda.
        """
        pass


    def print_command(
        self,
        print_job: PrintJobModel
    ):
        """
        Envia a comanda para impressão.
        """
        pass


    def save_backup(
        self,
        print_job: PrintJobModel
    ):
        """
        Salva PDF, preview, arte e metadados.
        """
        pass