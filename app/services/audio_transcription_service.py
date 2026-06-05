from faster_whisper import WhisperModel


class AudioTranscriptionService:
    def __init__(self) -> None:
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, file_path: str) -> str:
        segments, _ = self.model.transcribe(
            file_path,
            language="pt",
            beam_size=5,
        )

        full_text = ""
        for segment in segments:
            full_text += segment.text + " "

        return full_text.strip()