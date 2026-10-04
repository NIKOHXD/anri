"""Prepara il testo scritto da Anri per essere letto ad alta voce.

L'LLM a volte scrive simboli che, letti dalla voce sintetica, suonano male:
"24°C" diventerebbe "ventiquattro C", "**ciao**" "asterisco asterisco ciao".
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
    for vecchio, nuovo in SOSTITUZIONI.items():
        testo = testo.replace(vecchio, nuovo)
    return testo.strip()
