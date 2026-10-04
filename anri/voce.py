"""La "voce" di Anri: trasforma il testo in audio con Piper (text-to-speech)."""

from pathlib import Path

import numpy as np
import sounddevice as sd
from piper import PiperVoice
from piper.download_voices import download_voice

from anri import config


class Voce:
    """Carica la voce di Piper (scaricandola la prima volta) e la usa per parlare."""

    def __init__(self) -> None:
        cartella = Path(config.VOICES_DIR)
        file_voce = cartella / f"{config.PIPER_VOICE}.onnx"
        if not file_voce.exists():
            cartella.mkdir(exist_ok=True)
            download_voice(config.PIPER_VOICE, cartella)  # ~60 MB, solo la prima volta
        self.piper = PiperVoice.load(file_voce)

    def parla(self, testo: str) -> None:
        """Pronuncia il testo dalle casse e aspetta di aver finito di parlare."""
        if not testo.strip():
            return
        # Piper genera l'audio frase per frase: uniamo i pezzi in un unico array
        pezzi = list(self.piper.synthesize(testo))
        audio = np.concatenate([pezzo.audio_float_array for pezzo in pezzi])
        sd.play(audio, samplerate=pezzi[0].sample_rate)
        sd.wait()  # blocca finché l'audio non è finito
