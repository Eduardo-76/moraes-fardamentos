import sounddevice as sd
from scipy.io.wavfile import write

from pathlib import Path
from datetime import datetime


class AudioRecorder:

    def __init__(self):

        self.sample_rate = 44100

    def record(self, duration=5):

        print("🎤 Gravando...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1
        )

        sd.wait()

        print("✅ Finalizado")

        # pasta
        recordings_dir = Path("storage/recordings")
        recordings_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            datetime.now()
            .strftime("%Y%m%d_%H%M%S.wav")
        )

        filepath = recordings_dir / filename

        write(
            str(filepath),
            self.sample_rate,
            audio
        )

        return str(filepath)