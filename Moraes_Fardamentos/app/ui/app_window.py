import customtkinter as ctk
from app.core.config import APP_NAME
from app.core.database import initialize_database


def run_app() -> None:
    initialize_database()
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')

    app = ctk.CTk()
    app.title(APP_NAME)
    app.geometry('1200x700')

    label = ctk.CTkLabel(app, text=APP_NAME, font=('Arial', 24, 'bold'))
    label.pack(pady=40)

    subtitle = ctk.CTkLabel(app, text='Arquitetura inicial criada com sucesso.')
    subtitle.pack(pady=10)

    app.mainloop()


import customtkinter as ctk

from app.core.config import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_COLOR_THEME,
    DEFAULT_THEME,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
)
from app.ui.screens.dashboard_screen import DashboardScreen


class AppWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode(DEFAULT_THEME)
        ctk.set_default_color_theme(DEFAULT_COLOR_THEME)

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.minsize(1024, 600)

        self._build_layout()

    def _build_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Fardamento App",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            state="disabled",
        )
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=8, sticky="ew")

        self.orders_button = ctk.CTkButton(
            self.sidebar,
            text="Pedidos",
            state="disabled",
        )
        self.orders_button.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        self.stock_button = ctk.CTkButton(
            self.sidebar,
            text="Estoque",
            state="disabled",
        )
        self.stock_button.grid(row=3, column=0, padx=20, pady=8, sticky="ew")

        self.audio_button = ctk.CTkButton(
            self.sidebar,
            text="Áudios",
            state="disabled",
        )
        self.audio_button.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.dashboard_screen = DashboardScreen(self.main_frame)
        self.dashboard_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)