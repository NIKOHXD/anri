"""Test dell'esercizio 4."""

from anri.pulizia import pulisci_per_voce


def test_unita_di_misura():
    testo = "A Milano ci sono 24°C, vento a 6 km/h."
    assert pulisci_per_voce(testo) == "A Milano ci sono 24 gradi, vento a 6 chilometri orari."


def test_toglie_il_markdown():
    assert pulisci_per_voce("Ecco **la risposta** che cercavi") == "Ecco la risposta che cercavi"


def test_toglie_spazi_ai_bordi():
    assert pulisci_per_voce("## Titolo  ") == "Titolo"


def test_testo_normale_non_cambia():
    assert pulisci_per_voce("Ciao, come stai?") == "Ciao, come stai?"
