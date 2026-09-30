from pathlib import Path

from app.core.paths import APP_DIR


# Diretório onde o código/assets estão sendo executados.
# No projeto normal:
#   Moraes_Fardamentos/
#
# No EXE PyInstaller:
#   FardamentoApp/_internal/
BUNDLE_ROOT = Path(__file__).resolve().parents[2]


ASSETS_DIR = BUNDLE_ROOT / "assets"

TEMPLATES_DIR = ASSETS_DIR / "templates"

COMMAND_TEMPLATE = (
    TEMPLATES_DIR
    / "comanda_template.jpeg"
)


class PrintingPaths:

    @staticmethod
    def documents_folder(
        order_id: int
    ) -> Path:

        folder = (
            APP_DIR
            / "pedidos"
            / f"{order_id:06d}"
            / "documentos"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder

    @staticmethod
    def command_pdf(
        order_id: int
    ) -> Path:

        return (
            PrintingPaths.documents_folder(
                order_id
            )
            / "comanda.pdf"
        )

    @staticmethod
    def command_png(
        order_id: int
    ) -> Path:

        return (
            PrintingPaths.documents_folder(
                order_id
            )
            / "comanda.png"
        )

    @staticmethod
    def command_jpeg(
        order_id: int
    ) -> Path:

        return (
            PrintingPaths.documents_folder(
                order_id
            )
            / "comanda.jpg"
        )