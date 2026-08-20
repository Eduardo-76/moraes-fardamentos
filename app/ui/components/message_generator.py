import customtkinter as ctk
from tkinter import messagebox
from app.core.constants import MESSAGE_SECTORS

class MessageGenerator(ctk.CTkFrame):

    def __init__(
        self,
        master,
        order_service,
        order_id,
        copy_callback
    ):
        super().__init__(master)

        self.order_service = order_service
        self.order_id = order_id
        self.copy_callback = copy_callback

        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        title = ctk.CTkLabel(
            self,
            text="Gerar mensagem pronta",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=8,
            pady=(10, 15)
        )   

        controls = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        controls.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8
        )

        controls.grid_columnconfigure(
            1,
            weight=1
        )

        self.message_type = ctk.CTkOptionMenu(
            controls,
            values=[
                "Recepção",
                "Design",
                "Impressão",
                "Costura",
                "Entrega"
            ]
        )

        self.message_type.grid(
            row=0,
            column=0,
            padx=(0,10)
        )

        self.message_type.set("Recepção")

        generate_button = ctk.CTkButton(
            controls,
            text="Gerar mensagem",
            command=self.generate_message
        )

        generate_button.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self.output = ctk.CTkTextbox(
            self,
            height=180
        )

        self.output.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=8,
            pady=15
        )
        self.grid_rowconfigure(2, weight=1) 

        copy_button = ctk.CTkButton(
            self,
            text="Copiar mensagem",
            command=self.copy_message
        )

        copy_button.grid(
            row=3,
            column=0,
            sticky="w",
            padx=8,
            pady=(0,10)
        )

    def generate_message(self):
        sector = self.message_type.get()

        message = self.order_service.generate_stage_message(
            self.order_id,
            sector
        )

        self.output.delete("1.0", "end")
        self.output.insert("1.0", message)


    def copy_message(self):
        text = self.output.get(
            "1.0",
            "end"
        ).strip()

        if not text:
            messagebox.showwarning(
                "Aviso",
                "Nenhuma mensagem para copiar."
            )
            return

        self.copy_callback(text)