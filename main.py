"""Punto di ingresso: chat testuale con Anri nel terminale.

Avvio:  python main.py
Comandi speciali:  /reset (nuova conversazione)   /esci (chiude)
"""

import ollama
from rich.console import Console

from anri import config
from anri.brain import Brain

console = Console()


def show_tool_call(name: str, args: dict) -> None:
    """Mostra a schermo quale strumento sta usando Anri (utile per capire cosa succede)."""
    args_text = ", ".join(f"{k}={v!r}" for k, v in args.items())
    console.print(f"\n[dim]  ⚙ {name}({args_text})[/]")


def main() -> None:
    brain = Brain(on_tool_call=show_tool_call)
    console.print(f"[bold cyan]Anri[/] online[dim](modello: {config.MODEL})[/]")
    console.print("[dim]Scrivi un messaggio, /reset per ricominciare, /esci per uscire.[/]\n")

    while True:
        try:
            text = console.input("[bold green]Tu > [/]").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not text:
            continue
        if text == "/esci":
            break
        if text == "/reset":
            brain.reset()
            console.print("[dim]Memoria della conversazione cancellata.[/]\n")
            continue

        console.print("[bold cyan]Anri > [/]", end="")
        try:
            for piece in brain.ask(text):
                console.print(piece, end="", highlight=False)
        except ollama.ResponseError as e:
            console.print(f"\n[red]Errore dal modello: {e.error}[/]")
        except ConnectionError:
            console.print("\n[red]Ollama non risponde: è avviato?[/]")
        console.print("\n")

    console.print("[dim]Ciao![/]")


if __name__ == "__main__":
    main()
