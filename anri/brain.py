"""Il "cervello" di Anri: parla con l'LLM che gira in locale tramite Ollama."""

from collections.abc import Callable, Generator, Iterator
from typing import Any

import ollama
from ollama import Message

from anri import config
from anri.tools import TOOLS, esegui

# Funzione chiamata ogni volta che Anri usa uno strumento (es. per mostrarlo a schermo)
ToolCallback = Callable[[str, dict[str, Any]], None]


class Brain:
    """Gestisce la conversazione con l'LLM, la sua cronologia e l'uso degli strumenti."""

    def __init__(self, model: str = config.MODEL, on_tool_call: ToolCallback | None = None) -> None:
        self.model = model
        self.on_tool_call = on_tool_call
        self.history: list[Message] = []

    def ask(self, text: str) -> Iterator[str]:
        """Manda una domanda all'LLM e restituisce la risposta un pezzo alla volta.

        Come funziona il "tool calling":
          1. mandiamo all'LLM la conversazione + l'elenco degli strumenti disponibili
          2. l'LLM può rispondere con del testo, oppure chiedere di eseguire
             uno o più strumenti (es. meteo(citta="Roma"))
          3. se chiede strumenti, li eseguiamo noi, aggiungiamo i risultati alla
             conversazione e torniamo al punto 1: ora l'LLM può usarli per rispondere
        """
        self.history.append(Message(role="user", content=text))

        for _ in range(config.MAX_TOOL_ROUNDS):
            content, tool_calls = yield from self._stream_reply()
            self.history.append(
                Message(role="assistant", content=content, tool_calls=tool_calls or None)
            )
            if not tool_calls:
                return  # risposta finale: niente altro da fare

            for call in tool_calls:
                name, args = call.function.name, dict(call.function.arguments)
                if self.on_tool_call:
                    self.on_tool_call(name, args)
                result = esegui(name, args)
                self.history.append(Message(role="tool", content=result, tool_name=name))

        yield "(Interrotto: troppe azioni di fila per una sola richiesta.)"

    def _stream_reply(self) -> Generator[str, None, tuple[str, list[Message.ToolCall]]]:
        """Chiede una risposta all'LLM, passando il testo al chiamante man mano che arriva.

        Alla fine *restituisce* (con return, non yield) il testo completo e gli
        eventuali strumenti richiesti: li riceve chi usa `yield from`.
        """
        # think=False disattiva il "ragionamento" di Qwen3: risposte molto più
        # rapide, che per un assistente vocale contano più della profondità.
        stream = ollama.chat(
            model=self.model,
            messages=[Message(role="system", content=config.SYSTEM_PROMPT), *self._recent()],
            tools=list(TOOLS.values()),
            stream=True,
            think=False,
        )
        content = ""
        tool_calls: list[Message.ToolCall] = []
        for chunk in stream:
            if chunk.message.content:
                content += chunk.message.content
                yield chunk.message.content
            if chunk.message.tool_calls:
                tool_calls.extend(chunk.message.tool_calls)
        return content, tool_calls

    def _recent(self) -> list[Message]:
        """Gli ultimi messaggi della cronologia, partendo sempre da un messaggio dell'utente.

        Se tagliassimo a metà, la conversazione potrebbe iniziare con il risultato
        di uno strumento senza la richiesta che l'ha generato, confondendo l'LLM.
        """
        recent = self.history[-config.MAX_HISTORY :]
        while recent and recent[0].role != "user":
            recent = recent[1:]
        return recent

    def reset(self) -> None:
        """Dimentica la conversazione corrente."""
        self.history.clear()
