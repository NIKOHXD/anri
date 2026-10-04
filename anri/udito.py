"""L'"udito" di Anri: trasforma la voce in testo con Whisper (speech-to-text)."""

import importlib.util
import os
from pathlib import Path

import numpy as np

from anri import config


def _aggiungi_librerie_nvidia() -> None:
    """Fa trovare a Windows le librerie CUDA (cuBLAS e cuDNN) installate con pip.

    Su Windows i programmi cercano le DLL nelle cartelle elencate nella
    variabile d'ambiente PATH: aggiungiamo quelle dei pacchetti nvidia-*.
    """
    spec = importlib.util.find_spec("nvidia")
    if spec is None or not spec.submodule_search_locations:
        return  # pacchetti non installati: Whisper userà la CPU o darà errore
    base = Path(spec.submodule_search_locations[0])
    for libreria in ("cublas", "cudnn"):
        cartella = base / libreria / "bin"
        if cartella.exists():
            os.environ["PATH"] = str(cartella) + os.pathsep + os.environ["PATH"]


_aggiungi_librerie_nvidia()

# Importato DOPO aver sistemato il PATH, altrimenti non troverebbe le DLL
from faster_whisper import WhisperModel  # noqa: E402


class Udito:
    """Carica Whisper una volta sola e lo usa per trascrivere l'audio."""

    def __init__(self) -> None:
        # float16 = numeri a metà precisione: dimezza la memoria usata sulla GPU,
        # senza differenze percepibili nella qualità della trascrizione
        compute_type = "float16" if config.WHISPER_DEVICE == "cuda" else "int8"
        self.modello = WhisperModel(
            config.WHISPER_MODEL, device=config.WHISPER_DEVICE, compute_type=compute_type
        )

    def trascrivi(self, audio: np.ndarray) -> str:
        """Restituisce il testo pronunciato nell'audio ("" se non c'è voce)."""
        if len(audio) < config.SAMPLE_RATE // 4:  # meno di un quarto di secondo
            return ""
        segmenti, _ = self.modello.transcribe(
            audio,
            language="it",
            # VAD = Voice Activity Detection: scarta i tratti senza voce, così
            # Whisper non si "inventa" frasi sul rumore di fondo
            vad_filter=True,
        )
        # Whisper divide il testo in segmenti: li uniamo in un'unica frase
        return "".join(segmento.text for segmento in segmenti).strip()
