"""Test dell'esercizio 1.

`monkeypatch` è uno strumento di pytest che sostituisce temporaneamente una
funzione con una finta: così i test non aprono davvero le app, ma registrano
cosa sarebbe stato aperto. Anche l'elenco delle app installate è finto, così
i test danno lo stesso risultato su qualsiasi PC.
"""

import pytest

from anri.tools import app

APP_INSTALLATE_FINTE = {
    "discord": "com.squirrel.Discord.Discord",
    "google chrome": "Chrome",
    "steam": "Steam.exe",
}


@pytest.fixture
def aperte(monkeypatch):
    """Sostituisce le funzioni che aprono le app e restituisce la lista delle app 'aperte'."""
    lista = []
    monkeypatch.setattr(app.os, "startfile", lambda destinazione: lista.append(destinazione))
    monkeypatch.setattr(app, "apri_app_installata", lambda app_id: lista.append(app_id))
    monkeypatch.setattr(app, "trova_app_installate", lambda: APP_INSTALLATE_FINTE)
    return lista


def test_apre_scorciatoia(aperte):
    risposta = app.apri_app("calcolatrice")
    assert aperte == ["calc.exe"]
    assert risposta == "Ho aperto calcolatrice."


def test_ignora_maiuscole_e_spazi(aperte):
    app.apri_app("  Blocco Note ")
    assert aperte == ["notepad.exe"]


def test_apre_app_installata_nome_identico(aperte):
    risposta = app.apri_app("Discord")
    assert aperte == ["com.squirrel.Discord.Discord"]
    assert risposta == "Ho aperto discord."


def test_apre_app_installata_nome_parziale(aperte):
    app.apri_app("chrome")
    assert aperte == ["Chrome"]


def test_app_non_trovata(aperte):
    risposta = app.apri_app("macchina del tempo")
    assert aperte == []  # non deve aprire niente
    assert risposta == "Non ho trovato l'app macchina del tempo sul computer."
