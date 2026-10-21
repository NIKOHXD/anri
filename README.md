# Anri — assistente AI personale, 100% locale

Assistente vocale che gira interamente sul tuo PC: capisce cosa gli chiedi ed esegue
azioni sul computer. Niente cloud, niente abbonamenti, i tuoi dati restano tuoi.

## Come funziona

```
🎤 voce → Whisper (speech-to-text) → Qwen3 + strumenti → Piper (text-to-speech) → 🔊
```

| Componente | Tecnologia | Dove gira |
|---|---|---|
| Riconoscimento vocale | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) `large-v3-turbo` | GPU |
| Cervello | Qwen3 8B via [Ollama](https://ollama.com), con tool calling | GPU |
| Sintesi vocale | [Piper](https://github.com/OHF-Voice/piper1-gpl), voce italiana | CPU |

**Strumenti disponibili:** apre qualsiasi app installata, ora e data, timer e
promemoria, meteo in tempo reale (Open-Meteo).

## Stato del progetto

- [x] **Fase 1** — Chat testuale con un LLM locale (Qwen3 8B via Ollama)
- [x] **Fase 2** — Strumenti: apre app, ora/meteo, timer (tool calling)
- [x] **Fase 3** — Voce: speech-to-text (Whisper) e text-to-speech (Piper)
- [ ] **Fase 4** — Attivazione vocale con la parola "Anri"
- [ ] **Fase 5** — Memoria a lungo termine
- [ ] **Fase 6** — Interfaccia grafica

## Requisiti

- Windows o macOS, Python 3.12
- [Ollama](https://ollama.com) con il modello `qwen3:8b` (Windows) o `qwen3:4b-instruct` (macOS)
- Windows: GPU NVIDIA consigliata (sviluppato su RTX 5070 Ti, 16 GB)
- macOS: Apple Silicon. Whisper gira sulla CPU con il modello `small`
  (le impostazioni cambiano da sole in base al sistema, vedi `anri/config.py`)
- Microfono e cuffie/casse per la modalità vocale

## Installazione

Windows:

```bash
ollama pull qwen3:8b
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS:

```bash
brew install ollama && brew services start ollama
ollama pull qwen3:4b-instruct
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Sul Mac, al primo avvio della modalità vocale macOS chiede il permesso di usare
il microfono per il Terminale (o per VS Code).

## Uso

```bash
python main_voce.py   # modalità vocale: premi Invio, parla, premi Invio
python main.py        # modalità testuale
```

Al primo avvio vengono scaricati in automatico il modello Whisper (~1.6 GB su Windows, ~500 MB su macOS) e la
voce di Piper (~60 MB).

## Sviluppo

```bash
pip install -r requirements-dev.txt
python -m pytest      # test automatici
ruff check .          # controllo del codice
```
