import customtkinter as ctk


class AudioActionPreviewDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        parsed_data
    ):
        super().__init__(master)

        self.parsed_data = parsed_data

        self.title("Ação detectada")
        self.geometry("500x400")

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Ação detectada",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.pack(pady=(20, 10))

        content = ""

        for key, value in self.parsed_data.items():

            content += f"{key}: {value}\n"

        textbox = ctk.CTkTextbox(
            self,
            height=250
        )

        textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        textbox.insert(
            "1.0",
            content
        )

        textbox.configure(
            state="disabled"
        )

        close_btn = ctk.CTkButton(
            self,
            text="Fechar",
            command=self.destroy
        )

        close_btn.pack(
            pady=(0, 20)
        )