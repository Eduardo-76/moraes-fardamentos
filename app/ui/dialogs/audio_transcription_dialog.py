import customtkinter as ctk

from app.services.audio_parser_service import AudioParserService
from app.services.audio_transcription_service import AudioTranscriptionService
from app.ui.dialogs.audio_parse_result_dialog import AudioParseResultDialog


class AudioTranscriptionDialog(ctk.CTkToplevel):
    def __init__(self, master, audio, on_confirm=None) -> None:
        super().__init__(master)

        self.audio = audio
        self.on_confirm = on_confirm
        self.service = AudioTranscriptionService()
        self.parser_service = AudioParserService()

        self.title("Transcrição de Áudio")
        self.geometry("760x560")

        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._run_transcription()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self,
            text=self.audio.original_name,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.pack(pady=10)

        hint = ctk.CTkLabel(
            self,
            text=(
                "Dica: fale no formato → cliente, quantidade, produto, tamanhos e prazo.\n"
                "Ex: João, 30 camisas dryfit branca, 10 M masculina..."
            ),
            font=ctk.CTkFont(size=12),
            justify="center",
        )
        hint.pack(pady=(0, 10))

        self.textbox = ctk.CTkTextbox(self, height=320)
        self.textbox.pack(fill="both", expand=True, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Transcrevendo...")
        self.status_label.pack(pady=5)

        buttons = ctk.CTkFrame(self)
        buttons.pack(pady=10)

        confirm_btn = ctk.CTkButton(
            buttons,
            text="Confirmar",
            command=self._confirm,
        )
        confirm_btn.grid(row=0, column=0, padx=10)

        parse_btn = ctk.CTkButton(
            buttons,
            text="Extrair dados",
            command=self._parse_text,
        )
        parse_btn.grid(row=0, column=1, padx=10)

        cancel_btn = ctk.CTkButton(
            buttons,
            text="Cancelar",
            command=self.destroy,
        )
        cancel_btn.grid(row=0, column=2, padx=10)

    def _run_transcription(self):
        try:
            text = self.service.transcribe(self.audio.file_path)
            self.textbox.insert("1.0", text)
            self.status_label.configure(text="Transcrição pronta")
        except Exception as e:
            self.status_label.configure(text=f"Erro: {str(e)}")

    def _parse_text(self):
        text = self.textbox.get("1.0", "end").strip()
        parsed_data = self.parser_service.parse_order_text(text)
        parsed_data["audio_id"] = self.audio.id

        AudioParseResultDialog(
            self,
            parsed_data=parsed_data,
        )

    def _confirm(self):
        text = self.textbox.get("1.0", "end").strip()

        if callable(self.on_confirm):
            self.on_confirm(self.audio.id, text)

        self.destroy()