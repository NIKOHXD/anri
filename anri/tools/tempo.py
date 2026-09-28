"""Strumento di esempio: ora e data attuali.

Usalo come modello per i tuoi strumenti. Nota tre cose:
- la docstring è ciò che legge l'LLM per capire QUANDO usare lo strumento
- la funzione restituisce una stringa in linguaggio naturale
- la logica "pura" (formatta_data) è separata dalla parte che dipende
  dall'esterno (l'orologio del PC), così si può testare facilmente
"""

from datetime import datetime

from anri.tools.registry import tool

GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]  # fmt: skip


def formatta_data(momento: datetime) -> str:
    """Trasforma una data in una frase italiana, es. 'Sono le 18:05 di lunedì 28 settembre 2026.'"""
    giorno = GIORNI[momento.weekday()]  # weekday(): 0 = lunedì ... 6 = domenica
    mese = MESI[momento.month - 1]  # month va da 1 a 12, le liste partono da 0
    return f"Sono le {momento:%H:%M} di {giorno} {momento.day} {mese} {momento.year}."


@tool
def ora_e_data() -> str:
    """Restituisce l'ora e la data attuali.

    Usalo quando l'utente chiede che ore sono o che giorno è.
    """
    return formatta_data(datetime.now())
