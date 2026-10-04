"""Prepara il testo scritto da Anri per essere letto ad alta voce.

═══════════════════════════ ESERCIZIO 4 (facile) ═══════════════════════════
L'LLM a volte scrive simboli che, letti dalla voce sintetica, suonano male:
"24°C" diventa "ventiquattro C", "**ciao**" viene letto "asterisco asterisco ciao".

Implementa `pulisci_per_voce`. Deve:
  1. sostituire nel testo ogni chiave di SOSTITUZIONI con il suo valore
     ("24°C" -> "24 gradi", "**ciao**" -> "ciao")
  2. togliere gli spazi all'inizio e alla fine del risultato

Suggerimenti:
  - testo.replace("vecchio", "nuovo") restituisce una NUOVA stringa con tutte
    le sostituzioni (le stringhe in Python non si modificano: si ricreano)
  - per applicare tutte le sostituzioni ti serve un ciclo for su SOSTITUZIONI:
    ricordi .items() dall'esercizio delle app?

Verifica:  python -m pytest tests/test_pulizia.py
══════════════════════════════════════════════════════════════════════════════
"""

# Cosa cercare -> con cosa sostituirlo
SOSTITUZIONI = {
    "°C": " gradi",
    "km/h": "chilometri orari",
    "*": "",  # grassetto e corsivo in Markdown
    "#": "",  # titoli in Markdown
}


def pulisci_per_voce(testo: str) -> str:
    """Restituisce il testo pronto per la sintesi vocale."""
    # ✏️ Scrivi qui il tuo codice (e cancella la riga sotto)
    raise NotImplementedError
