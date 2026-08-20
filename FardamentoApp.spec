from PyInstaller.utils.hooks import collect_all


# =========================================================
# RECURSOS / MÓDULOS
# =========================================================

datas = []
binaries = []
hiddenimports = []


packages = [
    "customtkinter",
    "whisper",
    "torch",
    "torchaudio",
    "scipy",
    "sounddevice",
    "PIL",
    "pymupdf",
]


for package in packages:

    try:

        tmp_datas, tmp_binaries, tmp_hiddenimports = (
            collect_all(package)
        )

        datas += tmp_datas
        binaries += tmp_binaries
        hiddenimports += tmp_hiddenimports

    except Exception as exc:

        print(
            f"[WARN] Não foi possível coletar "
            f"{package}: {exc}"
        )


# =========================================================
# RECURSOS DO PROJETO
# =========================================================

datas += [
    ("assets", "assets"),
    ("docs", "docs"),
]


# =========================================================
# ANÁLISE
# =========================================================

a = Analysis(
    ["main.py"],

    pathex=[],

    binaries=binaries,

    datas=datas,

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,
)


# =========================================================
# PYZ
# =========================================================

pyz = PYZ(
    a.pure
)


# =========================================================
# EXECUTÁVEL
# =========================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],

    name="FardamentoApp",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=False,

    console=False,
)


# =========================================================
# COLLECT — ONEDIR
# =========================================================

coll = COLLECT(
    exe,

    a.binaries,

    a.datas,

    strip=False,

    upx=False,

    name="FardamentoApp",
)