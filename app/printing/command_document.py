from pathlib import Path

from PIL import Image


class CommandDocument:

    def __init__(
        self,
        image,
        order_id: int
    ):

        self._image = image
        self._order_id = order_id

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def image(self):
        return self._image

    def show(self):

        self._image.show()

    def save_png(
        self,
        path: str | Path
    ):

        self._image.save(path, "PNG")

    def save_pdf(
        self,
        path: str | Path,
        resolution: int = 300
    ):

        image = self._image.convert("RGB")

        image.save(
            path,
            "PDF",
            resolution=resolution
        )