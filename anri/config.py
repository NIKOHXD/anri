"""Impostazioni di Anri, tutte in un unico posto.

Quando vorrai cambiare modello o personalità, modifica solo questo file.
"""

import sys

# Su Windows Anri gira sul PC con la GPU NVIDIA; su macOS (Mac M2, 8 GB di RAM)
# usiamo modelli più leggeri che stanno nella memoria e girano senza CUDA.
SU_MAC = sys.platform == "darwin"

# Nome del modello scaricato con `ollama pull` (vedi `ollama list`).
# qwen3:8b occupa ~5 GB: su un Mac da 8 GB, insieme a Whisper, non ci sta bene.
# Serve la variante "instruct": "qwen3:4b" ragiona sempre (ignora think=False)
# e scriverebbe tutto il ragionamento nella risposta.
MODEL = "qwen3:4b-instruct" if SU_MAC else "qwen3:8b"

# Il "system prompt" definisce il comportamento dell'assistente: viene mandato
# all'LLM prima di ogni conversazione.
SYSTEM_PROMPT = """Sei Anri, un assistente personale che gira sul computer dell'utente.
Rispondi in italiano, in modo naturale e diretto, dando del tu.
Le risposte sono brevi (massimo 2-3 frasi) perché in futuro verranno lette
ad alta voce. Se non sai qualcosa, lo dici chiaramente.
Hai a disposizione degli strumenti: usali quando servono per rispondere o per
fare ciò che l'utente chiede. Puoi fare SOLO ciò che i tuoi strumenti permettono:
non inventare azioni e non dire di aver fatto qualcosa se uno strumento ha
restituito un errore."""

# Quanti messaggi recenti tenere in memoria durante una conversazione.
# Più messaggi = più contesto, ma risposte più lente.
MAX_HISTORY = 20

# Quante volte di fila Anri può usare strumenti per una singola richiesta,
# prima di fermarsi (evita cicli infiniti se il modello si "incastra").
MAX_TOOL_ROUNDS = 5

# --- Memoria a lungo termine (Fase 5) ---

# File dove Anri salva i fatti sull'utente (è personale: escluso da git)
MEMORIA_FILE = "memoria.json"

# --- Voce (Fase 3) ---

# Modello Whisper per capire cosa dici. "large-v3-turbo" è il migliore per
# l'italiano e sulla RTX 5070 Ti trascrive una frase in circa 0.2 secondi.
# Sul Mac non c'è CUDA: Whisper gira sulla CPU con il modello "small", più veloce.
WHISPER_MODEL = "small" if SU_MAC else "large-v3-turbo"
WHISPER_DEVICE = "cpu" if SU_MAC else "cuda"

# Voce italiana di Piper. Altre voci: https://rhasspy.github.io/piper-samples/
PIPER_VOICE = "it_IT-paola-medium"
VOICES_DIR = "voci"

# Whisper lavora con audio a 16000 campioni al secondo
SAMPLE_RATE = 16000
