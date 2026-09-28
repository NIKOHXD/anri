from anri.tools import TOOLS, esegui


def test_tutti_gli_strumenti_sono_registrati():
    assert {"ora_e_data", "apri_app", "imposta_timer", "meteo"} <= TOOLS.keys()


def test_esegui_strumento_inesistente():
    assert "non esiste" in esegui("vola", {})


def test_esegui_cattura_gli_errori():
    # Argomento sbagliato: invece di crashare, esegui restituisce un messaggio d'errore
    assert esegui("ora_e_data", {"parametro_inesistente": 1}).startswith("Errore")
