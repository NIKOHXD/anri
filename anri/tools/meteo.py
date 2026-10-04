"""Strumento: meteo attuale di una città, tramite le API gratuite di Open-Meteo.

═══════════════════════════ ESERCIZIO 3 (più impegnativo) ══════════════════
Implementa `meteo`. Servono due chiamate HTTP a Open-Meteo (gratis, senza chiave):

  1. GEOCODING: dal nome della città alle coordinate
       httpx.get(GEOCODING_URL, params={"name": citta, "count": 1, "language": "it"}, timeout=10)
     Risposta JSON (semplificata):
       {"results": [{"name": "Milano", "latitude": 45.46, "longitude": 9.19, ...}]}
     ⚠️ se la città non esiste, la chiave "results" MANCA del tutto.
        In quel caso restituisci una stringa che inizia con "Non ho trovato".

  2. METEO: dalle coordinate al meteo attuale
       httpx.get(METEO_URL, params={
           "latitude": ..., "longitude": ...,
           "current": "temperature_2m,weather_code,wind_speed_10m",
       }, timeout=10)
     Risposta JSON (semplificata):
       {"current": {"temperature_2m": 18.4, "weather_code": 1, "wind_speed_10m": 12.3}}

  3. Restituisci una frase con: nome della città (quello restituito dal
     geocoding), temperatura arrotondata all'intero, descrizione del cielo
     (usa DESCRIZIONI_METEO) e vento. Esempio:
       "A Milano ci sono 18°C, cielo prevalentemente sereno, vento a 12 km/h."

Suggerimenti:
  - risposta = httpx.get(...)  poi  risposta.raise_for_status()  (errore se il
    server risponde male)  poi  dati = risposta.json()  (diventa un dict Python)
  - dict.get("chiave") restituisce None invece di dare errore se la chiave manca
  - round(18.4) -> 18
  - codici non presenti nel dizionario: DESCRIZIONI_METEO.get(codice, "condizioni sconosciute")
  - prova le API nel browser, es.:
    https://geocoding-api.open-meteo.com/v1/search?name=Milano&count=1&language=it

Verifica:  .venv\\Scripts\\python.exe -m pytest tests/test_meteo.py
(i test non usano internet: simulano le risposte di Open-Meteo, quindi devi
usare httpx.get come indicato sopra)
══════════════════════════════════════════════════════════════════════════════
"""

import httpx

from anri.tools.registry import tool

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Codici meteo WMO usati da Open-Meteo -> descrizione in italiano
DESCRIZIONI_METEO = {
    0: "cielo sereno",
    1: "cielo prevalentemente sereno",
    2: "parzialmente nuvoloso",
    3: "coperto",
    45: "nebbia",
    48: "nebbia con brina",
    51: "pioviggine leggera",
    53: "pioviggine",
    55: "pioviggine intensa",
    61: "pioggia leggera",
    63: "pioggia",
    65: "pioggia forte",
    71: "neve leggera",
    73: "neve",
    75: "neve forte",
    80: "rovesci leggeri",
    81: "rovesci",
    82: "rovesci violenti",
    95: "temporale",
    96: "temporale con grandine",
    99: "temporale con grandine forte",
}


@tool
def meteo(citta: str) -> str:
    """Restituisce il meteo attuale di una città (temperatura, cielo, vento).

    Args:
        citta: nome della città, ad esempio "Milano" o "Parigi"
    """
    risposta = httpx.get(
        GEOCODING_URL, params={"name": citta, "count": 1, "language": "it"}, timeout=10
    )
    risposta.raise_for_status()
    dati = risposta.json()
    risultati = dati.get("results")

    if not risultati:
        return "Non ho trovato informazioni sul meteo per questa città."

    luogo = risultati[0]
    latitudine = luogo["latitude"]
    longitudine = luogo["longitude"]

    risposta_meteo = httpx.get(
        METEO_URL,
        params={
            "latitude": latitudine,
            "longitude": longitudine,
            "current": "temperature_2m,weather_code,wind_speed_10m",
        },
        timeout=10,
    )
    risposta_meteo.raise_for_status()
    attuale = risposta_meteo.json()

    temperature = round(attuale["current"]["temperature_2m"])
    cielo = DESCRIZIONI_METEO.get(attuale["current"]["weather_code"], "condizioni sconosciute")
    vento = round(attuale["current"]["wind_speed_10m"])

    return f"A {luogo['name']} ci sono {temperature}°C, {cielo}, vento a {vento} km/h."
