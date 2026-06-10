import customtkinter as ctk

from app.services.stock_service import StockService


class SelectStockDialog(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.result = None

        self.service = StockService()

        self.title("Selecionar Estoque")
        self.geometry("500x300")

        self.grab_set()

        title = ctk.CTkLabel(
            self,
            text="Selecione o estoque"
        )

        title.pack(
            pady=(20, 10)
        )

        self.stock_entries = (
            self.service.list_stock_entries()
        )

        values = []

        for stock in self.stock_entries:

            values.append(
                f"{stock.model} | {stock.type} | {stock.color}"
            )

        self.combo = ctk.CTkComboBox(
            self,
            values=values
        )

        self.combo.pack(
            fill="x",
            padx=20,
            pady=10
        )

        button = ctk.CTkButton(
            self,
            text="Selecionar",
            command=self._confirm
        )

        button.pack(
            pady=20
        )

    def _confirm(self):

        selected = self.combo.get()

        for stock in self.stock_entries:

            label = (
                f"{stock.model} | "
                f"{stock.type} | "
                f"{stock.color}"
            )

            if label == selected:

                self.result = stock.id
                break

        self.destroy()