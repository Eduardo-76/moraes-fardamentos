from pathlib import Path

from PIL import Image


class CommandDocument:

    def __init__(self, image, order_id: int):
        self._image = image
        self._order_id = order_id

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def image(self):
        return self._image

    def show(self):
        """
        Salva a comanda em arquivo permanente e abre esse arquivo.

        Não usa Image.show(), evitando os arquivos temporários
        tmp... que estavam chegando ao spooler do Windows.
        """
        path = self.save_jpeg()

        import os

        if os.name == "nt":
            os.startfile(str(path))
        else:
            self._image.show()

        return path

    def save_png(self, path: str | Path | None = None):
        if path is None:
            from app.printing.printing_paths import PrintingPaths
            path = PrintingPaths.command_png(self._order_id)

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        self._image.convert("RGB").save(path, "PNG")

        return path

    def save_jpeg(
        self,
        path: str | Path | None = None,
        quality: int = 95
    ):
        if path is None:
            from app.printing.printing_paths import PrintingPaths
            path = PrintingPaths.command_jpeg(self._order_id)

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        image = self._image.convert("RGB")

        image.save(
            path,
            "JPEG",
            quality=quality,
            optimize=True
        )

        return path

    def save_pdf(
        self,
        path: str | Path,
        resolution: int = 300
    ):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        image = self._image.convert("RGB")

        image.save(
            path,
            "PDF",
            resolution=resolution
        )

        return path
