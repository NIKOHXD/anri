"""Impostazioni di Anri, tutte in un unico posto.

Quando vorrai cambiare modello o personalità, modifica solo questo file.
"""

# Nome del modello scaricato con `ollama pull` (vedi `ollama list`).
MODEL = "qwen3:8b"

# Il "system prompt" definisce il comportamento dell'assistente: viene mandato
# all'LLM prima di ogni conversazione.
SYSTEM_PROMPT = """Sei Anri, un assistente personale che gira sul computer dell'utente.
Rispondi in italiano, in modo naturale e diretto, dando del tu.
Le risposte sono brevi (massimo 2-3 frasi) perché in futuro verranno lette
ad alta voce. Se non sai qualcosa, lo dici chiaramente.
Per ora puoi solo conversare: non puoi eseguire azioni sul computer né accedere
a internet, quindi non offrirti di farlo."""

# Quanti messaggi recenti tenere in memoria durante una conversazione.
# Più messaggi = più contesto, ma risposte più lente.
MAX_HISTORY = 20
