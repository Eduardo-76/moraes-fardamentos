from typing import List

from app.core.database import get_connection
from app.models.audio_model import AudioModel


class AudioRepository:
    def create_audio(self, audio: AudioModel) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO audios (original_name, file_name, file_path, notes)
                VALUES (?, ?, ?, ?)
                """,
                (
                    audio.original_name,
                    audio.file_name,
                    audio.file_path,
                    audio.notes,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def list_audios(self) -> List[AudioModel]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, original_name, file_name, file_path, notes, created_at
                FROM audios
                ORDER BY created_at DESC, id DESC
                """
            )
            rows = cursor.fetchall()

            return [
                AudioModel(
                    id=row["id"],
                    original_name=row["original_name"],
                    file_name=row["file_name"],
                    file_path=row["file_path"],
                    notes=row["notes"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]
        finally:
            connection.close()

    def delete_audio(self, audio_id: int) -> None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM audios WHERE id = ?", (audio_id,))
            connection.commit()
        finally:
            connection.close()