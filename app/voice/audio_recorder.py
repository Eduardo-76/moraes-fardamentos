import sounddevice as sd
from scipy.io.wavfile import write

from app.core.paths import RECORDINGS_DIR
from datetime import datetime

import numpy as np


class AudioRecorder:

    def __init__(self):
        self.sample_rate = 44100

        self.stream = None
        self.audio_chunks = []
        self.is_recording = False

    def start(self):
        if self.is_recording:
            return

        print("🎤 Gravando...")

        self.audio_chunks = []
        self.is_recording = True

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._audio_callback
        )

        self.stream.start()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)

        if self.is_recording:
            self.audio_chunks.append(indata.copy())

    def stop(self):
        if not self.is_recording:
            return None

        print("⏹️ Parando gravação...")

        self.is_recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.audio_chunks:
            print("⚠️ Nenhum áudio foi gravado.")
            return None

        audio = np.concatenate(self.audio_chunks, axis=0)

        recordings_dir = RECORDINGS_DIR

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

        print("✅ Finalizado")
        print(f"📁 Salvo em: {filepath}")

        return str(filepath)

    def record(self, duration=5):
        """
        Mantém compatibilidade com o método antigo.
        Grava por uma duração determinada.
        """

        self.start()

        sd.sleep(int(duration * 1000))

        return self.stop()