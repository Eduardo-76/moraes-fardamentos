from app.core.paths import ARTWORK_DIR

from app.printing.command_canvas import CommandCanvas
from app.printing.command_document import CommandDocument
from app.services.order_service import OrderService
from app.printing.printing_paths import (
    COMMAND_TEMPLATE,
    PrintingPaths
)


class CommandPrinter:

    def __init__(self):

        self.order_service = OrderService()

    def _get_artwork_path(
        self,
        order_id: int
    ):

        artwork_dir = ARTWORK_DIR

        if not artwork_dir.exists():
            return None

        extensions = [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".pdf"
        ]

        for extension in extensions:

            artwork_path = (
                artwork_dir
                / f"pedido_{order_id}{extension}"
            )

            if artwork_path.exists():
                return artwork_path

        return None

    def build(
        self,
        order_id: int
    ) -> CommandDocument:

        job = self.order_service.get_print_job(
            order_id
        )

        canvas = CommandCanvas()

        canvas.load_template(
            COMMAND_TEMPLATE
        )

        artwork_path = self._get_artwork_path(
            order_id
        )

        canvas.draw_print_job(
            job,
            artwork_path=artwork_path
        )

        return CommandDocument(
            image=canvas.get_image(),
            order_id=order_id
        )

    def preview(
        self,
        order_id: int
    ):

        document = self.build(
            order_id
        )

        document.show()

    def export_pdf(
        self,
        order_id: int
    ):

        document = self.build(
            order_id
        )

        document.save_pdf(
            PrintingPaths.command_pdf(
                order_id
            )
        )