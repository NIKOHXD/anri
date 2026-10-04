# Anri — assistente AI personale, 100% locale

Assistente vocale che gira interamente sul tuo PC: capisce cosa gli chiedi ed esegue
azioni sul computer. Niente cloud, niente abbonamenti, i tuoi dati restano tuoi.

## Stato del progetto

- [x] **Fase 1** — Chat testuale con un LLM locale (Qwen3 8B via Ollama)
- [x] **Fase 2** — Strumenti: apre app, ora/meteo, timer (tool calling)
- [ ] **Fase 3** — Voce: speech-to-text (Whisper) e text-to-speech (Piper)
- [ ] **Fase 4** — Attivazione vocale con la parola "Anri"
- [ ] **Fase 5** — Memoria a lungo termine
- [ ] **Fase 6** — Interfaccia grafica

## Requisiti

- Python 3.12
- [Ollama](https://ollama.com) con il modello `qwen3:8b`
- Consigliata una GPU NVIDIA (sviluppato su RTX 5070 Ti, 16 GB)

## Installazione

```bash
ollama pull qwen3:8b
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
