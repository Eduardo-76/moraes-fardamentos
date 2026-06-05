import shutil
import uuid
from pathlib import Path
from typing import List
import os
from app.core.config import AUDIO_DIR
from app.models.audio_model import AudioModel
from app.repositories.audio_repository import AudioRepository


class AudioService:
    def __init__(self) -> None:
        self.repository = AudioRepository()

    def import_audio(self, source_path: str, notes: str | None = None) -> int:
        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError("Arquivo de áudio não encontrado.")

        allowed_extensions = {".mp3", ".wav", ".m4a", ".ogg", ".opus", ".webm"}
        extension = source.suffix.lower()

        if extension not in allowed_extensions:
            raise ValueError("Formato de áudio não permitido.")

        AUDIO_DIR.mkdir(parents=True, exist_ok=True)

        new_file_name = f"{uuid.uuid4().hex}{extension}"
        destination = AUDIO_DIR / new_file_name

        shutil.copy2(source, destination)

        audio = AudioModel(
            original_name=source.name,
            file_name=new_file_name,
            file_path=str(destination),
            notes=notes,
        )

        return self.repository.create_audio(audio)

    def list_audios(self) -> List[AudioModel]:
        return self.repository.list_audios()

    def delete_audio(self, audio_id: int, file_path: str | None = None) -> None:
        self.repository.delete_audio(audio_id)

        if file_path:
            path = Path(file_path)
            if path.exists():
                path.unlink()

    def open_audio(self, file_path: str) -> None:
        if not file_path:
            return

        if os.path.exists(file_path):
            os.startfile(file_path)      

    def get_audio_by_id(self, audio_id: int):
        audios = self.list_audios()
        for audio in audios:
            if audio.id == audio_id:
                return audio
        return None  
    
    def open_audio(self, file_path: str) -> None:
        if not file_path:
            return

        if os.path.exists(file_path):
            os.startfile(file_path)