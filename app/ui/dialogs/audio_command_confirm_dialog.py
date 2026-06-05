import customtkinter as ctk


class AudioCommandConfirmDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        text,
        on_confirm=None
    ):
        super().__init__(master)

        self.on_confirm = on_confirm
        self.transcription = text

        self.title("Confirmar comando")
        self.geometry("500x300")

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Transcrição detectada",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.pack(pady=(20, 10))

        self.textbox = ctk.CTkTextbox(
            self,
            height=120
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.textbox.insert(
            "1.0",
            self.transcription
        )

        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons_frame.pack(
            pady=20
        )

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            fg_color="#DC2626",
            hover_color="#991B1B",
            command=self.destroy
        )

        cancel_btn.pack(
            side="left",
            padx=10
        )

        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Confirmar",
            command=self._confirm
        )

        confirm_btn.pack(
            side="left",
            padx=10
        )

    def _confirm(self):

        text = self.get_text()

        self.destroy()

        if self.on_confirm:

            self.after(
                100,
                lambda: self.on_confirm(text)
            )

    def get_text(self):

        return self.textbox.get(
            "1.0",
            "end"
        ).strip()