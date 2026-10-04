"""Anri in modalità vocale: parli al microfono e ti risponde a voce.

Avvio:  python main_voce.py
"""

from rich.console import Console

from anri.brain import Brain
from anri.microfono import registra
from anri.pulizia import pulisci_per_voce
from anri.udito import Udito
from anri.voce import Voce
from main import show_tool_call

console = Console()


def main() -> None:
    # Caricare i modelli richiede qualche secondo: lo facciamo UNA volta sola,
    # prima del ciclo, non a ogni frase.
    with console.status("Caricamento dei modelli..."):
        brain = Brain(on_tool_call=show_tool_call)
        udito = Udito()
        voce = Voce()

    console.print('[bold cyan]Anri[/] in ascolto. Dì [bold]"esci"[/] per chiudere.\n')

    while True:
        console.input("[dim]Premi Invio e parla...[/]")
        console.print("[bold red]● Registrazione[/] [dim](premi Invio quando hai finito)[/]")

        # 1. Dalla voce al testo
        audio = registra()
        testo = udito.trascrivi(audio)

        if not testo.strip():
            console.print("[dim]Non ho sentito niente, riprova.[/]")
            continue

        console.print(f"[bold green]Tu >[/] {testo}")

        # Confronto esatto, non `in`: "riesci a..." non deve chiudere il programma
        if testo.lower().strip(" .?!") == "esci":
            console.print("[dim]Uscita richiesta dall'utente.[/]")
            break

        # 2. Anri ragiona e usa gli strumenti. Per parlare serve la risposta completa,
        #    quindi uniamo i pezzi che brain.ask() restituisce man mano
        risposta = "".join(brain.ask(testo))
        console.print(f"[bold cyan]Anri >[/] {risposta}")

        # 3. Dal testo alla voce
        voce.parla(pulisci_per_voce(risposta))

    console.print("[dim]Ciao![/]")


if __name__ == "__main__":
    main()
