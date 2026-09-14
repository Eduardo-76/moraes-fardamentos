from datetime import datetime
from pathlib import Path

import fitz

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from app.printing.command_layout import (
    UNIT_VALUE,
    TextField,
    TextArea,
    CLIENT_NAME,
    PHONE,
    CITY,
    DELIVERY_DATE,
    CREATED_AT_LABEL,
    CREATED_AT_VALUE,
    MODEL,
    FABRIC,
    TYPE,
    TOTAL_VALUE,
    OBSERVATIONS,
    SIZE_LAYOUT,
    ARTWORK_AREA,
)



class CommandCanvas:

    def __init__(self):

        self.image = None
        self.draw = None

        self._font_cache = {}

        self.font_path = self._find_font()


    def _find_font(self):

        possible_fonts = [
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/calibri.ttf"),
            Path("C:/Windows/Fonts/segoeui.ttf"),
        ]

        for font_path in possible_fonts:

            if font_path.exists():
                return font_path

        return None


    def _get_font(
        self,
        font_size: int
    ):

        if font_size in self._font_cache:
            return self._font_cache[font_size]

        if self.font_path:

            font = ImageFont.truetype(
                str(self.font_path),
                font_size
            )

        else:

            font = ImageFont.load_default()

        self._font_cache[font_size] = font

        return font


    def load_template(
        self,
        template_file
    ):

        self.image = Image.open(
            template_file
        ).convert("RGB")

        self.draw = ImageDraw.Draw(
            self.image
        )

        return self.image


    def show(self):

        if self.image is None:

            raise RuntimeError(
                "Nenhum template carregado."
            )

        self.image.show()


    def draw_text(
        self,
        text,
        x,
        y,
        font_size=18
    ):

        if self.draw is None:

            raise RuntimeError(
                "Nenhum template carregado."
            )

        if text is None:
            return

        font = self._get_font(
            font_size
        )

        self.draw.text(
            (x, y),
            str(text),
            fill="black",
            font=font
        )


    def draw_field(
        self,
        text,
        field: TextField
    ):

        self.draw_text(
            text=text,
            x=field.x,
            y=field.y,
            font_size=field.font_size
        )

    def draw_currency(
        self,
        value,
        field: TextField
    ):

        try:
            numeric_value = float(value or 0)

        except (TypeError, ValueError):
            numeric_value = 0.0

        formatted_value = (
            f"R$ {numeric_value:,.2f}"
            .replace(",", "_")
            .replace(".", ",")
            .replace("_", ".")
        )

        self.draw_field(
            text=formatted_value,
            field=field
        )

    def draw_size(
        self,
        category,
        size,
        quantity
    ):
        position = SIZE_LAYOUT.get(
            category.strip().title(),
            {}

        ).get(size.strip().upper())
        if position is None:
            return

        self.draw_text(
            text=str(quantity),
            x=position.x,
            y=position.y,
            font_size=position.font_size
        )

    def draw_grades(
        self,
        grades
    ):

        for grade in grades:

            print(f"Grupo: {grade.group}")

            for item in grade.items:

                print(
                    f"  Tamanho: {item.size} | Quantidade: {item.quantity}"
                )

                self.draw_size(
                    category=grade.group,
                    size=item.size,
                    quantity=item.quantity
                )

    def draw_print_job(
        self,
        job,
        artwork_path=None
    ):
        """
        Desenha toda a comanda utilizando
        um PrintJobModel.
        """

        self.draw_field(
            job.client_name,
            CLIENT_NAME
        )

        self.draw_field(
            job.client_phone,
            PHONE
        )

        self.draw_field(
            job.client_city,
            CITY
        )

        self.draw_field(
            job.delivery_date,
            DELIVERY_DATE
        )

        if job.created_at:
            try:
                created_date = datetime.strptime(
                    str(job.created_at),
                    "%Y-%m-%d %H:%M:%S"
                )

                created_date_text = created_date.strftime(
                    "%d/%m/%Y"
                )

            except ValueError:
                created_date_text = str(job.created_at)

            self.draw_field(
                "DATA DE CRIAÇÃO",
                CREATED_AT_LABEL
            )

            self.draw_field(
                created_date_text,
                CREATED_AT_VALUE
            )


        self.draw_field(
            job.model,
            MODEL
        )

        self.draw_field(
            job.fabric,
            FABRIC
        )

        self.draw_field(
            job.type,
            TYPE
        )

        self.draw_currency(
            job.total_value,
            TOTAL_VALUE
        )

        self.draw_currency(
            job.unit_value,
            UNIT_VALUE
        )

        self.draw_text_area(
            job.observations,
            OBSERVATIONS
        )

        self.draw_grades(
            job.grades
        )

        self.draw_artwork(
            artwork_path
        )       

    def get_image(self):

        if self.image is None:
            raise RuntimeError(
                "Nenhuma imagem foi criada."
            )

        return self.image

    def draw_text_area(
        self,
        text,
        area: TextArea
    ):

        if self.draw is None:
            raise RuntimeError(
                "Nenhum template carregado."
            )

        if not text:
            return

        font = self._get_font(
            area.font_size
        )

        words = str(text).split()

        lines = []
        current_line = ""

        for word in words:

            test_line = (
                f"{current_line} {word}".strip()
            )

            bbox = self.draw.textbbox(
                (0, 0),
                test_line,
                font=font
            )

            text_width = bbox[2] - bbox[0]

            if text_width <= area.width:

                current_line = test_line

            else:

                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        y = area.y

        line_height = (
            area.font_size +
            area.line_spacing
        )

        max_lines = max(
            1,
            area.height // line_height
        )

        for line in lines[:max_lines]:

            self.draw.text(
                (area.x, y),
                line,
                fill="black",
                font=font
            )

            y += line_height

    def draw_artwork(
        self,
        artwork_path,
        area=ARTWORK_AREA
    ):

        if self.image is None:
            raise RuntimeError(
                "Nenhum template carregado."
            )

        if not artwork_path:
            return

        artwork_file = Path(
            artwork_path
        )

        if not artwork_file.exists():
            return

        extension = (
            artwork_file.suffix.lower()
        )

        # =====================================================
        # PDF
        # =====================================================

        if extension == ".pdf":

            document = fitz.open(
                str(artwork_file)
            )

            if document.page_count == 0:
                document.close()
                return

            page = document.load_page(0)

            pixmap = page.get_pixmap(
                alpha=True,
                matrix=fitz.Matrix(2, 2)
            )

            artwork = Image.frombytes(
                "RGBA",
                (
                    pixmap.width,
                    pixmap.height
                ),
                pixmap.samples
            )

            document.close()

        # =====================================================
        # IMAGENS
        # =====================================================

        else:

            artwork = Image.open(
                artwork_file
            ).convert("RGBA")

        # =====================================================
        # REDIMENSIONAMENTO
        # =====================================================

        artwork.thumbnail(
            (
                area.width,
                area.height
            ),
            Image.Resampling.LANCZOS
        )

        # =====================================================
        # CENTRALIZAÇÃO
        # =====================================================

        x = (
            area.x
            + (
                area.width
                - artwork.width
            ) // 2
        )

        y = (
            area.y
            + (
                area.height
                - artwork.height
            ) // 2
        )

        # =====================================================
        # INSERÇÃO
        # =====================================================

        self.image.paste(
            artwork,
            (x, y),
            artwork
        )