"""Strumento: timer e promemoria.

═══════════════════════════ ESERCIZIO 2 (medio) ════════════════════════════
Implementa `imposta_timer`. Deve:
  1. se `minuti` è <= 0, restituire una stringa che contiene
     "deve essere maggiore di zero" (senza avviare nessun timer)
  2. avviare un timer che, dopo `minuti` minuti, chiama notifica(promemoria)
  3. restituire subito una conferma, es. "Timer impostato: 5 minuti."
     (non deve aspettare che il timer scada!)

Suggerimenti:
  - threading.Timer(secondi, funzione, args=[argomento]) crea un timer che
    esegue la funzione in un thread separato; poi va avviato con .start()
    (concetto simile a std::thread in C++)
  - imposta `.daemon = True` sul timer prima di avviarlo: così, se chiudi Anri,
    il programma non resta bloccato ad aspettare i timer ancora attivi
  - attenzione: il timer vuole SECONDI, l'utente ti dà MINUTI

Bonus (facoltativo): nella conferma scrivi "30 secondi" se minuti < 1,
e "1 minuto" al singolare.

Verifica:  .venv\\Scripts\\python.exe -m pytest tests/test_timer.py
══════════════════════════════════════════════════════════════════════════════
"""

import threading  # noqa: F401  (ti servirà per l'esercizio)
import winsound

from rich.console import Console

from anri.tools.registry import tool

console = Console()


def notifica(promemoria: str) -> None:
    """Avvisa l'utente che un timer è scaduto (messaggio a schermo + suono)."""
    console.print(f"\n[bold yellow]⏰ {promemoria}[/]")
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)


@tool
def imposta_timer(minuti: float, promemoria: str = "Il timer è scaduto!") -> str:
    """Imposta un timer o un promemoria che avvisa l'utente dopo un certo numero di minuti.

    Args:
        minuti: dopo quanti minuti far scattare il timer (può essere decimale, es. 0.5 = 30 secondi)
        promemoria: il messaggio da mostrare quando il timer scade
    """
    # ✏️ Scrivi qui il tuo codice (e cancella la riga sotto)
    raise NotImplementedError
