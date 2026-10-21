"""Test dell'esercizio 4.

`tmp_path` è una cartella temporanea che pytest crea (vuota) per ogni test:
facciamo puntare la memoria lì, così i test non toccano la tua memoria vera.
"""

import json

import pytest

from anri import config
from anri.tools import ricordi


@pytest.fixture
def file_memoria(tmp_path, monkeypatch):
    """Usa un file di memoria temporaneo e restituisce una funzione per leggerlo."""
    percorso = tmp_path / "memoria.json"
    monkeypatch.setattr(config, "MEMORIA_FILE", str(percorso))

    def contenuto():
        return json.loads(percorso.read_text(encoding="utf-8")) if percorso.exists() else []

    return contenuto


def test_ricorda_salva_il_fatto(file_memoria):
    assert ricordi.ricorda("Studia informatica") == "Ok, me lo ricorderò."
    assert file_memoria() == ["Studia informatica"]


def test_ricorda_toglie_gli_spazi(file_memoria):
    ricordi.ricorda("   Ama la pizza  ")
    assert file_memoria() == ["Ama la pizza"]


def test_ricorda_aggiunge_in_fondo(file_memoria):
    ricordi.ricorda("Si chiama Nicolò")
    ricordi.ricorda("Studia informatica")
    assert file_memoria() == ["Si chiama Nicolò", "Studia informatica"]


def test_ricorda_rifiuta_fatto_vuoto(file_memoria):
    assert "vuoto" in ricordi.ricorda("   ")
    assert file_memoria() == []


def test_ricorda_non_duplica(file_memoria):
    ricordi.ricorda("Ama la pizza")
    assert ricordi.ricorda("ama la PIZZA") == "Lo sapevo già."
    assert file_memoria() == ["Ama la pizza"]


def test_dimentica_toglie_i_fatti_giusti(file_memoria):
    ricordi.ricorda("Ama la Pizza")
    ricordi.ricorda("Studia informatica")
    ricordi.ricorda("La pizza preferita è la margherita")
    risposta = ricordi.dimentica("pizza")
    assert risposta == "Ho dimenticato: Ama la Pizza; La pizza preferita è la margherita."
    assert file_memoria() == ["Studia informatica"]


def test_dimentica_argomento_sconosciuto(file_memoria):
    ricordi.ricorda("Studia informatica")
    assert ricordi.dimentica("calcio") == "Non ricordavo niente su calcio."
    assert file_memoria() == ["Studia informatica"]


def test_dimentica_argomento_vuoto_non_cancella_niente(file_memoria):
    ricordi.ricorda("Studia informatica")
    assert "vuoto" in ricordi.dimentica("   ")
    assert file_memoria() == ["Studia informatica"]
