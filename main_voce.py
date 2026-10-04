"""Anri in modalità vocale: parli al microfono e ti risponde a voce.

Avvio:  python main_voce.py

═══════════════════════════ ESERCIZIO 5 (il grande finale) ═══════════════════
Collega i pezzi! Tutto quello che ti serve è già importato qui sotto:
  - registra()                 -> registra dal microfono finché premi Invio (anri/microfono.py)
  - udito.trascrivi(audio)     -> trasforma l'audio in testo (anri/udito.py)
  - brain.ask(testo)           -> la risposta di Anri, a pezzi (anri/brain.py)
  - pulisci_per_voce(testo)    -> il TUO esercizio 4 (anri/pulizia.py)
  - voce.parla(testo)          -> legge il testo ad alta voce (anri/voce.py)

Segui i passi numerati dentro il ciclo `while` in main().
══════════════════════════════════════════════════════════════════════════════
"""

from rich.console import Console

from anri.brain import Brain
from anri.microfono import registra  # noqa: F401  (ti servirà)
from anri.pulizia import pulisci_per_voce  # noqa: F401  (ti servirà)
from anri.udito import Udito
from anri.voce import Voce
from main import show_tool_call

console = Console()


def main() -> None:
    # Caricare i modelli richiede qualche secondo: lo facciamo UNA volta sola,
    # prima del ciclo, non a ogni frase.
    with console.status("Caricamento dei modelli..."):
        brain = Brain(on_tool_call=show_tool_call)  # noqa: F841  (ti servirà)
        udito = Udito()  # noqa: F841  (ti servirà)
        voce = Voce()  # noqa: F841  (ti servirà)

    console.print('[bold cyan]Anri[/] in ascolto. Dì [bold]"esci"[/] per chiudere.\n')

    while True:
        console.input("[dim]Premi Invio e parla...[/]")
        console.print("[bold red]● Registrazione[/] [dim](premi Invio quando hai finito)[/]")

        # ✏️ PASSO 1: registra l'audio dal microfono e salvalo in una variabile

        # ✏️ PASSO 2: trascrivi l'audio in testo con udito.trascrivi(...)

        # ✏️ PASSO 3: se il testo è vuoto (non hai detto niente), torna all'inizio
        #             del ciclo. Suggerimento: la parola chiave `continue`

        # ✏️ PASSO 4: stampa cosa hai detto, es. console.print(f"[bold green]Tu >[/] {...}")

        # ✏️ PASSO 5: se nel testo c'è la parola "esci", esci dal ciclo (`break`)
        #             Attenzione: Whisper scrive "Esci." con maiuscola e punto!

        # ✏️ PASSO 6: chiedi la risposta ad Anri. brain.ask(...) restituisce la
        #             risposta a pezzi: uniscili in un'unica stringa con "".join(...)

        # ✏️ PASSO 7: stampa la risposta di Anri

        # ✏️ PASSO 8: falla pronunciare a voce, dopo averla ripulita

        break  # ✏️ cancella questa riga quando hai scritto i passi sopra

    console.print("[dim]Ciao![/]")


if __name__ == "__main__":
    main()
