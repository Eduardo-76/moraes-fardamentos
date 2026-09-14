from dataclasses import dataclass


@dataclass(frozen=True)
class TextField:
    x: int
    y: int
    font_size: int = 18


@dataclass(frozen=True)
class TextArea:
    x: int
    y: int
    width: int
    height: int
    font_size: int = 18
    line_spacing: int = 6


@dataclass(frozen=True)
class ImageField:
    x: int
    y: int
    width: int
    height: int

# =========================================================
# DADOS DO CLIENTE
# =========================================================

CLIENT_NAME = TextField(
    x=555,
    y=25,
    font_size=22,
)

PHONE = TextField(
    x=520,
    y=85,
    font_size=22,
)

CITY = TextField(
    x=555,
    y=143,
    font_size=22
)

DELIVERY_DATE = TextField(
    x=710,
    y=202,
    font_size=22
)

# =========================================================
# DADOS DO PEDIDO
# =========================================================

MODEL = TextField(
    x=430,
    y=950
)

FABRIC = TextField(
    x=430,
    y=930
)

TYPE = TextField(
    x=430,
    y=910
)

# =========================================================
# VALORES
# =========================================================

UNIT_VALUE = TextField(
    x=1150,
    y=45,
    font_size=20
)

TOTAL_VALUE = TextField(
    x=1150,
    y=125,
    font_size=20
)

CREATED_AT_LABEL = TextField(
    x=1400,
    y=35,
    font_size=15
)

CREATED_AT_VALUE = TextField(
    x=1415,
    y=62,
    font_size=18
)

# =========================================================
# OBSERVAÇÕES
# =========================================================

OBSERVATIONS = TextArea(
    x=430,
    y=970,
    width=820,
    height=160,
    font_size=18,
    line_spacing=6
)

# =========================================================
# ARTE
# =========================================================

ARTWORK_AREA = ImageField(
    x=455,
    y=300,
    width=800,
    height=500
)

# =========================================================
# GRADE DE TAMANHOS
# =========================================================

SIZE_LAYOUT = {

    "Masc": {

        "PP": TextField(x=110, y=364),
        "P":  TextField(x=110, y=408),
        "PK": TextField(x=110, y=450),
        "M":  TextField(x=110, y=494),
        "G":  TextField(x=110, y=536),
        "GG": TextField(x=110, y=578),
        "XGG": TextField(x=130, y=620),
    },

    "Femi": {

        "PP": TextField(110, 703),
        "P": TextField(110, 745),
        "M": TextField(110, 790),
        "G": TextField(110, 830),
        "GG": TextField(110, 873),
        "XGG": TextField(130, 916),
    },

    "Infantil": {

        "PP": TextField(97, 1003),
        "P":  TextField(97, 1045),

        "M":  TextField(210, 1003),
        "G":  TextField(210, 1045),
    }

}