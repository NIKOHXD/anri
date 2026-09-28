"""Il "cervello" di Anri: parla con l'LLM che gira in locale tramite Ollama."""

from collections.abc import Iterator

import ollama

from anri import config


class Brain:
    """Gestisce la conversazione con l'LLM e ne ricorda la cronologia."""

    def __init__(self, model: str = config.MODEL) -> None:
        self.model = model
        # La cronologia è una lista di messaggi nel formato che Ollama si aspetta:
        # {"role": "system" | "user" | "assistant", "content": "..."}
        self.history: list[dict[str, str]] = []

    def ask(self, text: str) -> Iterator[str]:
        """Manda una domanda all'LLM e restituisce la risposta un pezzo alla volta.

        È un *generatore* (nota lo `yield`): chi lo chiama riceve il testo
        mentre viene generato, come in ChatGPT, invece di aspettare la fine.
        """
        self.history.append({"role": "user", "content": text})

        messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]
        messages += self.history[-config.MAX_HISTORY :]

        # think=False disattiva il "ragionamento" di Qwen3: risposte molto più
        # rapide, che per un assistente vocale contano più della profondità.
        stream = ollama.chat(model=self.model, messages=messages, stream=True, think=False)

        answer = ""
        for chunk in stream:
            piece = chunk.message.content or ""
            answer += piece
            yield piece

        self.history.append({"role": "assistant", "content": answer})

    def reset(self) -> None:
        """Dimentica la conversazione corrente."""
        self.history.clear()
