"""Strumento: aprire applicazioni sul PC.

═══════════════════════════ ESERCIZIO 1 (facile) ═══════════════════════════
Implementa `apri_app`. Deve:
  1. normalizzare il nome ricevuto: minuscolo e senza spazi all'inizio/fine
     ("  Calcolatrice " -> "calcolatrice")
  2. se il nome NON è nel dizionario APP, restituire una stringa che inizia con
     "Non conosco l'app" e che elenca le app disponibili
  3. altrimenti aprire l'app con os.startfile(...) e restituire
     "Ho aperto <nome>."

Suggerimenti:
  - metodi delle stringhe: .lower(), .strip()
  - controllare se una chiave è in un dizionario: `if chiave in dizionario:`
  - unire una lista di stringhe: ", ".join(lista)
  - os.startfile("calc.exe") è l'equivalente di fare doppio clic su un file
  - aggiungi a APP i programmi che usi (Discord, Steam, VS Code...)

Verifica:  .venv\\Scripts\\python.exe -m pytest tests/test_app.py
══════════════════════════════════════════════════════════════════════════════
"""

import os  # noqa: F401  (ti servirà per l'esercizio)

from anri.tools.registry import tool

# Nome detto dall'utente -> cosa passare a os.startfile.
# Può essere un eseguibile, un percorso completo, un URL o un "protocollo"
# come "spotify:" (funziona se l'app è installata).
APP = {
    "calcolatrice": "calc.exe",
    "blocco note": "notepad.exe",
    "esplora file": "explorer.exe",
    "browser": "https://www.google.com",
    "spotify": "spotify:",
}


@tool
def apri_app(nome: str) -> str:
    """Apre un'applicazione sul computer dell'utente.

    Args:
        nome: nome dell'applicazione da aprire, ad esempio "calcolatrice" o "spotify"
    """
    # ✏️ Scrivi qui il tuo codice (e cancella la riga sotto)
    raise NotImplementedError
