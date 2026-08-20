
from unittest import result

import customtkinter as ctk
from tkinter import filedialog
from app.ui.dialogs.audio_transcription_dialog import AudioTranscriptionDialog
from app.services.audio_service import AudioService
from app.voice.audio_recorder import AudioRecorder
from app.voice.speech_to_text import SpeechToTextService
from app.ui.dialogs.audio_command_confirm_dialog import AudioCommandConfirmDialog
from app.voice.intent_parser import IntentParser
from app.ui.dialogs.audio_action_preview_dialog import AudioActionPreviewDialog
from app.services.fabric_roll_service import FabricRollService

from app.ui.dialogs.fabric_voice_confirm_dialog import (
    FabricVoiceConfirmDialog
)

from app.ui.dialogs.fabric_voice_exit_dialog import (
    FabricVoiceExitDialog
)

from app.ui.dialogs.fabric_voice_transfer_dialog import (
    FabricVoiceTransferDialog
)

import unicodedata
from app.ui.dialogs.fabric_voice_order_dialog import FabricVoiceOrderDialog
from app.ui.dialogs.order_form_dialog import OrderFormDialog

from app.ui.dialogs.fabric_voice_selection_dialog import (
    FabricVoiceSelectionDialog
)


class AudioScreen(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.audio_service = AudioService()
        self.audio_recorder = AudioRecorder()
        self.speech_to_text_service = SpeechToTextService()
        self.intent_parser = IntentParser()
        self.fabric_roll_service = FabricRollService()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.is_recording = False
        self.recording_seconds = 0
        self.recording_timer = None
        self.record_button = None

        self._build_header()
        self._build_list()
        self.refresh_audios()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Assistente Operacional",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Use voz ou arquivos de áudio para executar ações no sistema. por WhatsApp, ligação ou gravações internas.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        import_button = ctk.CTkButton(
            header,
            text="Importar áudio",
            command=self._import_audio,
        )
        import_button.grid(row=0, column=1, rowspan=2, padx=16, pady=16, sticky="e")

        self.record_button = ctk.CTkButton(
            header,
            text="🎤 Gravar",
            command=self._toggle_recording,
            fg_color="#16A34A",
            hover_color="#15803D"
        )

        self.record_button.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(0, 16),
            pady=16,
            sticky="e"
        )

    def _build_list(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.list_frame.grid_columnconfigure(0, weight=1)

    def refresh_audios(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        audios = self.audio_service.list_audios()

        if not audios:
            label = ctk.CTkLabel(
                self.list_frame,
                text="Nenhum áudio importado ainda.",
                font=ctk.CTkFont(size=15),
            )
            label.grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        for index, audio in enumerate(audios):
            card = self._create_audio_card(audio)
            card.grid(row=index, column=0, sticky="ew", padx=8, pady=8)

    def _create_audio_card(self, audio) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.list_frame)
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text=audio.original_name or "Áudio sem nome",
            font=ctk.CTkFont(size=19, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Arquivo interno: {audio.file_name}\n"
                f"Data: {audio.created_at or 'Não informada'}\n"
                f"Observação: {audio.notes or 'Nenhuma'}"
            ),
            justify="left",
            font=ctk.CTkFont(size=13),
        )
        details.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        delete_button = ctk.CTkButton(
            frame,
            text="Excluir",
            width=100,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=lambda aid=audio.id, path=audio.file_path: self._delete_audio(aid, path),
        )

        transcribe_button = ctk.CTkButton(
            frame,
            text="Transcrever",
            width=100,
            command=lambda a=audio: self._open_transcription(a),
        )
        transcribe_button.grid(row=0, column=1, padx=16, pady=(16, 6), sticky="e")

        delete_button.grid(row=1, column=1, padx=16, pady=(0, 16), sticky="e")

        return frame

    def _import_audio(self) -> None:
        
        file_path = filedialog.askopenfilename(
            title="Selecione um áudio",
            filetypes=[
                ("Arquivos de áudio", "*.mp3 *.wav *.m4a *.ogg *.opus *.webm"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if not file_path:
            return

        try:
            self.audio_service.import_audio(file_path)
            self.refresh_audios()
        except Exception as error:
            self._show_error(str(error))

    def _delete_audio(self, audio_id: int, file_path: str | None) -> None:
        self.audio_service.delete_audio(audio_id, file_path)
        self.refresh_audios()

    def _show_error(self, message: str) -> None:
        error_window = ctk.CTkToplevel(self)
        error_window.title("Erro")
        error_window.geometry("520x220")
        error_window.transient(self)
        error_window.grab_set()

        label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=460,
            font=ctk.CTkFont(size=14),
        )
        label.pack(padx=24, pady=(30, 20))

        close_button = ctk.CTkButton(
            error_window,
            text="Fechar",
            command=error_window.destroy,
        )
        close_button.pack(pady=(0, 20))

    def _open_transcription(self, audio):
        AudioTranscriptionDialog(
            self,
            audio=audio,
            on_confirm=self._handle_transcription_confirm,
        )

    def _handle_transcription_confirm(self, audio_id: int, text: str):
        print("TRANSCRIÇÃO CONFIRMADA:", text)

    def _toggle_recording(self):

        if self.is_recording:
            self._stop_recording()
        else:
            self._start_recording()


    def _start_recording(self):

        if self.is_recording:
            return

        print("🎤 Iniciando gravação...")

        self.is_recording = True
        self.recording_seconds = 0

        self.audio_recorder.start()

        self.record_button.configure(
            text="⏹️ Parar (00:00)",
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )

        self._update_recording_timer()


    def _stop_recording(self):

        if not self.is_recording:
            return

        print("⏹️ Encerrando gravação...")

        self.is_recording = False

        if self.recording_timer is not None:
            self.after_cancel(
                self.recording_timer
            )
            self.recording_timer = None

        self.record_button.configure(
            text="⏳ Processando...",
            state="disabled",
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        )

        filepath = self.audio_recorder.stop()

        if not filepath:

            self.record_button.configure(
                text="🎤 Gravar",
                state="normal",
                fg_color="#16A34A",
                hover_color="#15803D"
            )

            return

        print("Áudio salvo:")
        print(filepath)

        print("Transcrevendo...")

        try:

            text = self.speech_to_text_service.transcribe(
                filepath
            )

            AudioCommandConfirmDialog(
                self,
                text,
                on_confirm=self._handle_confirmed_command
            )

        except Exception as error:

            self._show_error(
                str(error)
            )

        finally:

            self.record_button.configure(
                text="🎤 Gravar",
                state="normal",
                fg_color="#16A34A",
                hover_color="#15803D"
            )


    def _update_recording_timer(self):

        if not self.is_recording:
            return

        minutes = self.recording_seconds // 60
        seconds = self.recording_seconds % 60

        self.record_button.configure(
            text=(
                f"⏹️ Parar "
                f"({minutes:02d}:{seconds:02d})"
            )
        )

        self.recording_seconds += 1

        self.recording_timer = self.after(
            1000,
            self._update_recording_timer
        )


    def _handle_confirmed_command(
        self,
        text
    ):

        result = self.intent_parser.parse(text)

        print(result)

        # -----------------------------------
        # ENTRADA DE MALHA
        # -----------------------------------

        if result["intent"] == "fabric_entry":

            rolls = (
                self.fabric_roll_service
                .find_similar_rolls(
                    result["fabric_name"]
                )
            )

            location = (
                result.get("to_location")
                or "Depósito"
            )

            FabricVoiceSelectionDialog(
                self,
                rolls=rolls,
                quantity=result["quantity"],
                fabric_name=result["fabric_name"],
                location=location,
                on_confirm=self._confirm_fabric_entry
            )

            return

        # -----------------------------------
        # PEDIDO
        # -----------------------------------

        if result["intent"] == "create_order":

            FabricVoiceOrderDialog(
                self,
                client_name=result.get("client_name"),
                quantity=result.get("quantity"),
                product_name=result.get("product_name"),
                on_confirm=lambda: self._execute_order(result)
            )

            return

        # fallback
        AudioActionPreviewDialog(
            self,
            result
        )

        # -----------------------------------
        # SAÍDA DE MALHA
        # -----------------------------------

        if result["intent"] == "fabric_exit":

            self.fabric_roll_service.find_by_name(
                result["fabric_name"]
            )

            roll = self.fabric_roll_service.find_by_name(
                result["fabric_name"]
            )

            if not roll:
                print("Malha não encontrada")
                return

            FabricVoiceExitDialog(
                self,
                roll=roll,
                quantity=result["quantity"],
                on_confirm=self._execute_fabric_exit
            )

        # -----------------------------------
        # TRANSFERÊNCIA
        # -----------------------------------

        if result["intent"] == "fabric_transfer":

            roll = self.fabric_roll_service.find_by_name(
                result["fabric_name"]
            )

            if not roll:

                print("Malha não encontrada")
                return

            FabricVoiceTransferDialog(
                self,
                roll=roll,
                quantity=result["quantity"],
                to_location=result["to_location"],
                on_confirm=self._execute_fabric_transfer
            )
            return
     

    def _execute_fabric_entry(
        self,
        roll,
        location,
        quantity
    ):

        location = self._normalize_text(location)

        target_found = False

        for loc in roll.locations:

            if self._normalize_text(
                loc.location_name
            ) == location:

                loc.quantity += quantity
                target_found = True
                break

        if not target_found:

            from app.models.fabric_roll_model import (
                FabricRollLocation
            )

            roll.locations.append(
                FabricRollLocation(
                    location_name=location,
                    quantity=quantity
                )
            )

        roll.total_quantity += quantity

        self.fabric_roll_service.update_roll(
            roll
        )

        self.fabric_roll_service.register_entry(
            roll.id,
            location,
            quantity
        )

        print(
            f"Entrada realizada: "
            f"{quantity} unidades em {location}"
        )

    def _execute_fabric_exit(
        self,
        roll,
        quantity
    ):

        for loc in roll.locations:

            if loc.location_name == "Depósito":

                if loc.quantity < quantity:

                    print("Estoque insuficiente")
                    return

                loc.quantity -= quantity

        roll.total_quantity -= quantity

        self.fabric_roll_service.update_roll(
            roll
        )

        self.fabric_roll_service.register_exit(
            roll.id,
            "Depósito",
            quantity
        )

        print("Saída realizada com sucesso")

    def _execute_fabric_transfer(
        self,
        roll,
        quantity,
        from_location,
        to_location
    ):
        

        print("======== LOCATIONS ========")

        for loc in roll.locations:

            print(
                loc.location_name,
                loc.quantity
            )       

        from_location = from_location

        source_found = False
        target_found = False

        # -----------------------------------
        # REMOVE DA ORIGEM
        # -----------------------------------

        for loc in roll.locations:

            if (
                self._normalize_text(
                    loc.location_name
                )
                ==
                self._normalize_text(
                    from_location
                )
            ):

                source_found = True

                if loc.quantity < quantity:

                    print("Estoque insuficiente")
                    return

                loc.quantity -= quantity

                print(
                    "Comparando:",
                    loc.location_name,
                    from_location
                )

        print(
            "Nova quantidade:",
            loc.quantity
        )


        # -----------------------------------
        # ADICIONA DESTINO
        # -----------------------------------

        for loc in roll.locations:

            if (
                self._normalize_text(
                    loc.location_name
                )
                                ==
                self._normalize_text(
                    to_location
                )
            ):

                target_found = True
                loc.quantity += quantity

        # -----------------------------------
        # CRIA DESTINO SE NÃO EXISTIR
        # -----------------------------------

        if not target_found:

            from app.models.fabric_roll_model import (
                FabricRollLocation
            )

            roll.locations.append(
                FabricRollLocation(
                    location_name=to_location,
                    quantity=quantity
                )
            )

        # -----------------------------------
        # SALVA
        # -----------------------------------

        self.fabric_roll_service.update_roll(
            roll
        )

        self.fabric_roll_service.register_transfer(
            roll.id,
            from_location,
            to_location,
            quantity
        )

        print("Transferência realizada")

    def _normalize_text(self, text):

        text = unicodedata.normalize(
            "NFKD",
            text
        )

        text = text.encode(
            "ASCII",
            "ignore"
        ).decode("utf-8")

        return text.strip().lower()
    
    def _execute_order(self, command):

        OrderFormDialog(
            self,

            initial_data={

                "client_name": command.get(
                    "client_name"
                ),

                "city": command.get(
                    "city"
                ),

                "quantity": command.get(
                    "quantity"
                ),

                "model": command.get(
                    "model"
                ) or command.get(
                    "product_name"
                ),

                "order_type": command.get(
                    "order_type"
                ),

                "fabric": command.get(
                    "fabric"
                ),

                "deadline": command.get(
                    "deadline"
                ),

                "items": command.get(
                    "items",
                    []
                ),

                "raw_text": command.get(
                    "raw_text"
                ),
            },

            on_save=lambda order_id: print(
                f"Pedido {order_id} criado"
            )
        )

    def _confirm_fabric_entry(
        self,
        roll,
        quantity,
        location
    ):

        FabricVoiceConfirmDialog(
            self,
            roll=roll,
            quantity=quantity,
            location=location,
            on_confirm=self._execute_fabric_entry
        )

