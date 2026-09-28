"""Test dell'esercizio 3.

Invece di chiamare davvero internet, sostituiamo httpx.get con una funzione
finta che restituisce risposte preconfezionate, come farebbe Open-Meteo.
"""

import pytest

from anri.tools import meteo


class FintaRisposta:
    """Imita l'oggetto risposta di httpx con i due metodi che ti servono."""

    def __init__(self, dati):
        self._dati = dati

    def raise_for_status(self):
        pass

    def json(self):
        return self._dati


def finto_open_meteo(url, params=None, **kwargs):
    if url == meteo.GEOCODING_URL:
        if params["name"].lower() == "milano":
            return FintaRisposta(
                {"results": [{"name": "Milano", "latitude": 45.46, "longitude": 9.19}]}
            )
        return FintaRisposta({"generationtime_ms": 0.5})  # nessun "results"!
    if url == meteo.METEO_URL:
        assert params["latitude"] == 45.46 and params["longitude"] == 9.19
        return FintaRisposta(
            {"current": {"temperature_2m": 18.4, "weather_code": 1, "wind_speed_10m": 12.3}}
        )
    raise AssertionError(f"URL inatteso: {url}")


@pytest.fixture(autouse=True)
def niente_internet(monkeypatch):
    monkeypatch.setattr(meteo.httpx, "get", finto_open_meteo)


def test_meteo_citta_esistente():
    risposta = meteo.meteo("milano")
    assert "Milano" in risposta
    assert "18" in risposta and "18.4" not in risposta  # temperatura arrotondata
    assert "prevalentemente sereno" in risposta
    assert "12" in risposta  # vento


def test_meteo_citta_inesistente():
    assert meteo.meteo("Atlantide").startswith("Non ho trovato")
