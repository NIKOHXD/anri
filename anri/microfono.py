"""Registrazione dal microfono.

Come funziona l'audio digitale: il microfono misura la pressione dell'aria
migliaia di volte al secondo. Ogni misura è un numero (un "campione") tra -1 e 1.
Con SAMPLE_RATE = 16000, un secondo di voce è un array di 16000 numeri.
"""

import numpy as np
import sounddevice as sd

from anri import config


def registra() -> np.ndarray:
    """Registra dal microfono predefinito finché l'utente non preme Invio.

    Restituisce l'audio come array numpy di numeri decimali (float32).
    """
    blocchi: list[np.ndarray] = []

    def ricevi_blocco(dati: np.ndarray, *_) -> None:
        # sounddevice chiama questa funzione da un altro thread ogni pochi
        # millisecondi, passandole il nuovo pezzetto di audio. Lo mettiamo da parte.
        blocchi.append(dati.copy())

    # "with" apre il microfono e lo richiude da solo alla fine del blocco,
    # anche in caso di errore (come un distruttore in C++, il pattern RAII).
    with sd.InputStream(
        samplerate=config.SAMPLE_RATE, channels=1, dtype="float32", callback=ricevi_blocco
    ):
        input()  # il thread principale aspetta Invio, intanto la registrazione continua

    if not blocchi:
        return np.zeros(0, dtype=np.float32)
    # Uniamo i pezzetti in un solo array; [:, 0] prende l'unico canale (mono)
    return np.concatenate(blocchi)[:, 0]
