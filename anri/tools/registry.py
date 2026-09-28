"""Registro degli strumenti: tiene l'elenco delle funzioni che Anri può chiamare."""

from collections.abc import Callable
from typing import Any

# Nome della funzione -> funzione. È un dizionario "globale" del modulo:
# ogni volta che un file usa il decoratore @tool, la funzione finisce qui.
TOOLS: dict[str, Callable[..., Any]] = {}


def tool(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decoratore che registra una funzione come strumento di Anri.

    Uso:
        @tool
        def mia_funzione(parametro: str) -> str:
            ...

    Scrivere `@tool` sopra una funzione equivale a scrivere, dopo di essa,
    `mia_funzione = tool(mia_funzione)`. La funzione non viene modificata:
    viene solo aggiunta al registro.
    """
    TOOLS[func.__name__] = func
    return func


def esegui(nome: str, argomenti: dict[str, Any]) -> str:
    """Esegue lo strumento `nome` con gli argomenti scelti dall'LLM.

    Restituisce sempre una stringa, anche in caso di errore: il risultato viene
    rimandato all'LLM, che così può spiegare all'utente cosa è andato storto
    invece di far crashare il programma.
    """
    func = TOOLS.get(nome)
    if func is None:
        return f"Errore: lo strumento '{nome}' non esiste."
    try:
        # **argomenti "spacchetta" il dizionario in parametri con nome:
        # {"citta": "Roma"} diventa func(citta="Roma")
        return str(func(**argomenti))
    except NotImplementedError:
        return f"Errore: lo strumento '{nome}' non è ancora stato implementato."
    except Exception as e:
        return f"Errore durante l'esecuzione di '{nome}': {e}"
