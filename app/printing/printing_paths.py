from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ASSETS_DIR = PROJECT_ROOT / "assets"

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
            PROJECT_ROOT
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