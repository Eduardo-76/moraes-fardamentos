import whisper


class SpeechToTextService:

    def __init__(self):

        print("Carregando Whisper...")

        self.model = whisper.load_model("base")

        print("Whisper carregado!")

    def transcribe(self, audio_path):

        result = self.model.transcribe(
            audio_path,
            language="pt"
        )

        return result["text"]