import customtkinter as ctk

from app.repositories.order_stock_reservation_repository import (
    OrderStockReservationRepository,
)

from tkinter import messagebox
from app.services.stock_service import StockService
from app.ui.dialogs.order_stock_withdraw_dialog import (
    OrderStockWithdrawDialog
)
from app.services.order_service import OrderService



class StockReservationsDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        stock_entry_id: int
    ):
        super().__init__(master)

        self.title("Reservas do Estoque")
        self.geometry("700x500")

        self.repository = (
            OrderStockReservationRepository()
        )
        self.stock_service = StockService()
        self.order_service = OrderService()

        self.stock_entry_id = stock_entry_id

        self._build()

    def _build(self):

        title = ctk.CTkLabel(
            self,
            text="Reservas Ativas",
            font=("Arial", 20, "bold")
        )
        title.pack(
            pady=15
        )

        self.content = ctk.CTkScrollableFrame(
            self
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self._load_reservations()

    def _load_reservations(self):

        reservations = (
            self.repository.list_by_stock(
                self.stock_entry_id
            )
        )

        if not reservations:

            empty_label = ctk.CTkLabel(
                self.content,
                text="Nenhuma reserva encontrada."
            )

            empty_label.pack(
                pady=20
            )

            return

        grouped = {}

        for reservation in reservations:

            order_id = reservation["order_id"]

            if order_id not in grouped:

                grouped[order_id] = {
                    "client_name": reservation["client_name"],
                    "order_id": order_id,
                    "items": [],
                    "reservation_ids": []
                }

            grouped[order_id]["items"].append(
                reservation
            )
            grouped[order_id]["reservation_ids"].append(
                reservation["id"]
            )

        for order_data in grouped.values():

            card = self._create_reservation_card(
                order_data
            )

            card.pack(
                fill="x",
                padx=10,
                pady=5
            )




    def _create_reservation_card(
        self,
        order_data
    ):
        frame = ctk.CTkFrame(
            self.content
        )

        title = ctk.CTkLabel(
            frame,
            text=order_data["client_name"],
            font=("Arial", 18, "bold")
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        details_text = (
            f"Pedido #{order_data['order_id']}\n\n"
            "Itens reservados:\n"
        )

        total_reserved = 0

        for item in order_data["items"]:

            details_text += (
                f"• {item['size']} "
                f"{item['gender']} "
                f"- {item['quantity']}\n"
            )

            total_reserved += item["quantity"]

        details_text += (
            f"\nTotal reservado: "
            f"{total_reserved}"
        )

        details = ctk.CTkLabel(
            frame,
            justify="left",
            text=details_text
        )

        details.pack(
            anchor="w",
            padx=10,
            pady=(0, 10)
        )


        buttons_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        buttons_frame.pack(
            anchor="w",
            padx=10,
            pady=(0, 10)
        )

        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar Reserva",
            command=lambda ids=order_data["reservation_ids"]:
                self._cancel_group(ids)
        )

        cancel_button.pack(
            side="right",
            padx=10
        )

        withdraw_button = ctk.CTkButton(
            buttons_frame,
            text="Baixar Reserva",
            fg_color="#16A34A",
            hover_color="#15803D",
            command=lambda oid=order_data["order_id"]:
                self._withdraw_order(oid)
        )

        withdraw_button.pack(
            side="left",
            padx=(0, 10)
        )
            
        return frame
    

    def _cancel_reservation(
        self,
        reservation_id: int
    ):

        confirm = messagebox.askyesno(
            "Cancelar Reserva",
            "Deseja realmente cancelar esta reserva?"
        )

        if not confirm:
            return

        try:

            self.stock_service.cancel_reservation(
                reservation_id
            )

            self.destroy()

            new_dialog = StockReservationsDialog(
                self.master,
                self.stock_entry_id
            )

            self.master.wait_window(
                new_dialog
            )

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )

    def _cancel_group(
        self,
        reservation_ids
    ):

        confirm = messagebox.askyesno(
            "Cancelar Reserva",
            "Deseja realmente cancelar TODAS as reservas deste pedido?"
        )

        if not confirm:
            return

        try:

            for reservation_id in reservation_ids:

                self.stock_service.cancel_reservation(
                    reservation_id
                )

            self.destroy()

            new_dialog = StockReservationsDialog(
                self.master,
                self.stock_entry_id
            )

            self.master.wait_window(
                new_dialog
            )

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )

    def _withdraw_order(
        self,
        order_id: int
    ):

        confirm = messagebox.askyesno(
            "Baixar Reserva",
            (
                "Deseja realmente baixar "
                "todo o estoque reservado "
                "deste pedido?"
            )
        )

        if not confirm:
            return

        try:

            self.order_service.withdraw_reserved_stock(
                order_id
            )

            self._reload_reservations()

            messagebox.showinfo(
                "Sucesso",
                "Estoque baixado com sucesso."
            )

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )

    def _reload_reservations(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self._load_reservations()