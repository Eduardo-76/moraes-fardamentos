import customtkinter as ctk
from app.ui.screens.audio_screen import AudioScreen
from app.ui.screens.fabric_roll_history_screen import FabricRollHistoryScreen

from app.core.config import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_COLOR_THEME,
    DEFAULT_THEME,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
)
from app.services.order_service import OrderService
from app.services.stock_service import StockService
from app.ui.screens.dashboard_screen import DashboardScreen
from app.ui.screens.order_detail_screen import OrderDetailScreen
from app.ui.screens.orders_screen import OrdersScreen
from app.ui.screens.stock_screen import StockScreen
from app.ui.screens.fabric_roll_screen import FabricRollScreen
from app.ui.screens.security_screen import SecurityScreen
from app.ui.screens.order_management_screen import (
    OrderManagementScreen
)
from app.ui.screens.withdrawals_screen import WithdrawalsScreen

class AppWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode(DEFAULT_THEME)
        ctk.set_default_color_theme(DEFAULT_COLOR_THEME)

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.minsize(1024, 600)

        self.order_service = OrderService()
        self.stock_service = StockService()

        self.order_service.create_sample_orders_if_empty()
        self.stock_service.create_sample_stock_if_empty()

        self.current_screen = None

        self._build_layout()
        self.show_dashboard()

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
            command=self.show_dashboard,
        )
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=8, sticky="ew")

        self.orders_button = ctk.CTkButton(
            self.sidebar,
            text="Pedidos",
            command=self.show_orders,
        )
        self.orders_button.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        self.withdrawals_button = ctk.CTkButton(
            self.sidebar,
            text="Retiradas",
            command=self.show_withdrawals,
        )

        self.withdrawals_button.grid(
            row=3,
            column=0,
            padx=20,
            pady=8,
            sticky="ew",
        )

        self.stock_button = ctk.CTkButton(
            self.sidebar,
            text="Estoque",
            command=self.show_stock,
        )
        self.stock_button.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        self.audio_button = ctk.CTkButton(
            self.sidebar,
            text="Assistente",
            command=self.show_audio,
        )
        self.audio_button.grid(row=5, column=0, padx=20, pady=8, sticky="ew")

        self.fabric_roll_button = ctk.CTkButton(
            self.sidebar,
            text="Rolos de Malha",
            command=self.show_fabric_rolls,
        )
        self.fabric_roll_button.grid(row=6, column=0, padx=20, pady=8, sticky="ew")

        self.fabric_roll_history_button = ctk.CTkButton(
            self.sidebar,
            text="Histórico Malha",
            command=self.show_fabric_roll_history,
        )
        self.fabric_roll_history_button.grid(row=7, column=0, padx=20, pady=8, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.security_button = ctk.CTkButton(
            self.sidebar,
            text="🛠 Administração",
            command=self.show_security,
        )

        self.security_button.grid(
            row=8,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

    def _clear_main_frame(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self) -> None:
        self._clear_main_frame()
        self.current_screen = DashboardScreen(self.main_frame)
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_orders(self) -> None:
        self._clear_main_frame()
        self.current_screen = OrdersScreen(
            self.main_frame,
            on_open_order=self.show_order_detail,
        )
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_order_detail(self, order_id: int) -> None:
        self._clear_main_frame()
        self.current_screen = OrderDetailScreen(
            self.main_frame,
            order_id=order_id,
            on_back=self.show_orders,
        )
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_stock(self) -> None:
        self._clear_main_frame()
        self.current_screen = StockScreen(self.main_frame)
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_audio(self) -> None:
        self._clear_main_frame()
        self.current_screen = AudioScreen(self.main_frame)
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_fabric_rolls(self):
        self._clear_main_frame()
        self.current_screen = FabricRollScreen(self.main_frame)
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_fabric_roll_history(self):
        self._clear_main_frame()
        self.current_screen = FabricRollHistoryScreen(self.main_frame)
        self.current_screen.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def show_security(self):
        self._clear_main_frame()

        self.current_screen = SecurityScreen(
            self.main_frame
        )

        self.current_screen.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=16,
            pady=16
        )

    def show_order_management(self):
        self._clear_main_frame()

        self.current_screen = OrderManagementScreen(
            self.main_frame
        )

        self.current_screen.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=16,
            pady=16
        )

    def show_withdrawals(self) -> None:
        self._clear_main_frame()

        self.current_screen = WithdrawalsScreen(
            self.main_frame,
            on_open_order=self.show_order_detail_from_withdrawals,
        )

        self.current_screen.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=16,
            pady=16,
        )

    def show_order_detail_from_withdrawals(
        self,
        order_id: int,
    ) -> None:
        self._clear_main_frame()

        self.current_screen = OrderDetailScreen(
            self.main_frame,
            order_id=order_id,
            on_back=self.show_withdrawals,
        )

        self.current_screen.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=16,
            pady=16,
        )