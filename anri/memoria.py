"""Memoria a lungo termine di Anri: i fatti sull'utente, salvati su disco.

La "memoria" della conversazione (Brain.history) si cancella quando chiudi Anri.
Questa invece resta: è un semplice file JSON con una lista di frasi, ad esempio
    ["Si chiama Nicolò", "Studia informatica", "Il suo colore preferito è il blu"]

All'inizio di ogni richiesta i fatti vengono aggiunti al system prompt, così
l'LLM li "sa" senza doverli cercare.
"""

import json
from pathlib import Path

from anri import config


def carica() -> list[str]:
    """Legge i fatti salvati. Se il file non esiste ancora, la memoria è vuota."""
    percorso = Path(config.MEMORIA_FILE)
    if not percorso.exists():
        return []
    return json.loads(percorso.read_text(encoding="utf-8"))


def salva(fatti: list[str]) -> None:
    """Scrive i fatti su disco, sostituendo quelli che c'erano prima."""
    percorso = Path(config.MEMORIA_FILE)
    # ensure_ascii=False lascia le lettere accentate leggibili nel file ("è" e non "è")
    percorso.write_text(json.dumps(fatti, ensure_ascii=False, indent=2), encoding="utf-8")


def componi_prompt(fatti: list[str]) -> str:
    """Il system prompt completo: quello di base più i fatti ricordati (se ce ne sono)."""
    if not fatti:
        return config.SYSTEM_PROMPT
    elenco = "\n".join(f"- {fatto}" for fatto in fatti)
    return f"{config.SYSTEM_PROMPT}\n\nCose che sai sull'utente:\n{elenco}"
