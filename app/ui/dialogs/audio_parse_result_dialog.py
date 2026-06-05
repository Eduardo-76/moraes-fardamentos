import customtkinter as ctk

from app.ui.dialogs.order_form_dialog import OrderFormDialog


class AudioParseResultDialog(ctk.CTkToplevel):
    def __init__(self, master, parsed_data: dict) -> None:
        super().__init__(master)

        self.parsed_data = parsed_data

        self.title("Dados extraídos do áudio")
        self.geometry("760x620")
        self.minsize(680, 520)

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Dados extraídos do áudio",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.pack(pady=(20, 8))

        subtitle = ctk.CTkLabel(
            self,
            text="Revise os dados antes de usar para criar um pedido.",
            font=ctk.CTkFont(size=13),
        )
        subtitle.pack(pady=(0, 12))

        text_box = ctk.CTkTextbox(self, height=420)
        text_box.pack(fill="both", expand=True, padx=20, pady=10)

        text_box.insert("1.0", self._format_parsed_data())
        text_box.configure(state="disabled")

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=(0, 20))

        create_button = ctk.CTkButton(
            buttons,
            text="Criar pedido",
            command=self._create_order,
        )
        create_button.grid(row=0, column=0, padx=8)

        close_button = ctk.CTkButton(
            buttons,
            text="Fechar",
            command=self.destroy,
            fg_color="#374151",
            hover_color="#1F2937",
        )
        close_button.grid(row=0, column=1, padx=8)

    def _create_order(self) -> None:
        OrderFormDialog(
            self,
            initial_data={
                "audio_id": self.parsed_data.get("audio_id"),
                "client_name": self.parsed_data.get("client_name"),
                "quantity": self.parsed_data.get("quantity"),
                "model": self.parsed_data.get("model"),
                "fabric": self.parsed_data.get("fabric"),
                "color": self.parsed_data.get("color"),
                "deadline_text": self.parsed_data.get("deadline_text"),
                "raw_text": self.parsed_data.get("raw_text"),
                "items": self.parsed_data.get("items", []),
            },
        )

    def _format_parsed_data(self) -> str:
        items = self.parsed_data.get("items", [])

        lines = [
            f"Cliente: {self.parsed_data.get('client_name') or 'Não identificado'}",
            f"Quantidade total: {self.parsed_data.get('quantity') or 0}",
            f"Modelo: {self.parsed_data.get('model') or 'Não identificado'}",
            f"Tecido: {self.parsed_data.get('fabric') or 'Não identificado'}",
            f"Cor: {self.parsed_data.get('color') or 'Não identificada'}",
            f"Prazo falado: {self.parsed_data.get('deadline_text') or 'Não identificado'}",
            "",
            "Itens:",
        ]

        if items:
            for item in items:
                lines.append(
                    f"- {item.get('quantity')} {item.get('size')} - {item.get('gender')}"
                )
        else:
            lines.append("- Nenhum item identificado")

        lines.extend(["", "Texto original:", self.parsed_data.get("raw_text") or ""])

        return "\n".join(lines)