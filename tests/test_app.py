"""Test dell'esercizio 1.

`monkeypatch` è uno strumento di pytest che sostituisce temporaneamente una
funzione con una finta: così i test non aprono davvero le app, ma registrano
cosa sarebbe stato aperto.
"""

import pytest

from anri.tools import app


@pytest.fixture
def aperte(monkeypatch):
    """Sostituisce os.startfile con una funzione finta e restituisce la lista delle app 'aperte'."""
    lista = []
    monkeypatch.setattr(app.os, "startfile", lambda destinazione: lista.append(destinazione))
    return lista


def test_apre_app_conosciuta(aperte):
    risposta = app.apri_app("calcolatrice")
    assert aperte == ["calc.exe"]
    assert risposta == "Ho aperto calcolatrice."


def test_ignora_maiuscole_e_spazi(aperte):
    app.apri_app("  Blocco Note ")
    assert aperte == ["notepad.exe"]


def test_app_sconosciuta(aperte):
    risposta = app.apri_app("macchina del tempo")
    assert aperte == []  # non deve aprire niente
    assert risposta.startswith("Non conosco l'app")
    assert "calcolatrice" in risposta  # deve elencare le app disponibili
