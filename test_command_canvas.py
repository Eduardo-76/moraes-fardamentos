from app.printing.command_canvas import CommandCanvas

from app.printing.printing_paths import COMMAND_TEMPLATE

from app.printing.command_layout import (
    CLIENT_NAME,
    PHONE,
    CITY,
    DELIVERY_DATE,

    MODEL,
    FABRIC,
    TYPE,

    UNIT_VALUE,
    TOTAL_VALUE,

    OBSERVATIONS,
)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

canvas = CommandCanvas()

canvas.load_template(
    COMMAND_TEMPLATE
)


# ============================================================
# DADOS DO CLIENTE
# ============================================================

canvas.draw_field(
    "Eduardo",
    CLIENT_NAME
)

canvas.draw_field(
    "(86) 99999-9999",
    PHONE
)

canvas.draw_field(
    "Piracuruca - PI",
    CITY
)

canvas.draw_field(
    "18/08/2026",
    DELIVERY_DATE
)


# ============================================================
# DADOS DO PEDIDO
# ============================================================

canvas.draw_field(
    "Normal",
    MODEL
)

canvas.draw_field(
    "PP BRANCA",
    FABRIC
)

canvas.draw_field(
    "Estampada Toda",
    TYPE
)


# ============================================================
# VALORES
# ============================================================

canvas.draw_currency(
    35,
    UNIT_VALUE
)

canvas.draw_currency(
    1925,
    TOTAL_VALUE
)


# ============================================================
# OBSERVAÇÕES
# ============================================================

canvas.draw_field(
    "Pedido de teste. Todas as peças devem seguir o modelo informado.",
    OBSERVATIONS
)


# ============================================================
# GRADE — MASCULINO
# ============================================================

canvas.draw_size(
    "Masc",
    "PP",
    0
)

canvas.draw_size(
    "Masc",
    "P",
    0
)

canvas.draw_size(
    "Masc",
    "PK",
    0
)

canvas.draw_size(
    "Masc",
    "M",
    10
)

canvas.draw_size(
    "Masc",
    "G",
    0
)

canvas.draw_size(
    "Masc",
    "GG",
    0
)

canvas.draw_size(
    "Masc",
    "XGG",
    0
)


# ============================================================
# GRADE — FEMININO
# ============================================================

canvas.draw_size(
    "Femi",
    "PP",
    0
)

canvas.draw_size(
    "Femi",
    "P",
    30
)

canvas.draw_size(
    "Femi",
    "M",
    10
)

canvas.draw_size(
    "Femi",
    "G",
    0
)

canvas.draw_size(
    "Femi",
    "GG",
    0
)

canvas.draw_size(
    "Femi",
    "XGG",
    0
)


# ============================================================
# GRADE — INFANTIL
# ============================================================

canvas.draw_size(
    "Infantil",
    "PP",
    0
)

canvas.draw_size(
    "Infantil",
    "P",
    0
)

canvas.draw_size(
    "Infantil",
    "M",
    5
)

canvas.draw_size(
    "Infantil",
    "G",
    0
)


# ============================================================
# EXIBIR
# ============================================================

canvas.show()