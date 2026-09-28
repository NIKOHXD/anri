"""Test dell'esercizio 2."""

import threading
import time

import pytest

from anri.tools import timer


class Notifiche(list):
    """Lista dei promemoria ricevuti, più un evento per aspettare che il timer scatti."""

    def __init__(self):
        super().__init__()
        self.scattato = threading.Event()


@pytest.fixture
def notifiche(monkeypatch):
    """Sostituisce notifica() con una versione finta che registra i promemoria ricevuti."""
    ricevute = Notifiche()

    def finta_notifica(promemoria):
        ricevute.append(promemoria)
        ricevute.scattato.set()

    monkeypatch.setattr(timer, "notifica", finta_notifica)
    return ricevute


def test_rifiuta_minuti_non_positivi(notifiche):
    assert "deve essere maggiore di zero" in timer.imposta_timer(0)
    assert "deve essere maggiore di zero" in timer.imposta_timer(-3)
    assert notifiche == []


def test_risponde_subito_senza_aspettare(notifiche):
    inizio = time.monotonic()
    risposta = timer.imposta_timer(10, "pasta")
    assert time.monotonic() - inizio < 1  # non deve bloccarsi per 10 minuti!
    assert "10" in risposta


def test_il_timer_scatta_con_il_promemoria(notifiche):
    timer.imposta_timer(0.001, "Scola la pasta")  # 0.001 minuti = 0.06 secondi
    assert notifiche.scattato.wait(timeout=2), "il timer non è scattato"
    assert notifiche == ["Scola la pasta"]
