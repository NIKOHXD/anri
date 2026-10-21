"""Strumento: aprire applicazioni sul PC.

═══════════════════════ ESERCIZIO 1b: tutte le app del PC ══════════════════════
Ora apri_app deve cercare, oltre che in APP, tra TUTTE le app installate.
Ordine di ricerca:
  1. se il nome è in APP (le scorciatoie scritte a mano) -> apri quella
  2. altrimenti cercalo tra le app installate (trova_app_installate()):
     a. prima un nome IDENTICO          ("discord"  -> "discord")
     b. poi un nome che lo CONTIENE      ("chrome"   -> "google chrome")
     e aprila con apri_app_installata(app_id)
  3. se non trovi niente: "Non ho trovato l'app <nome> sul computer."
Il messaggio di successo resta: "Ho aperto <nome>."

Verifica:  python -m pytest tests/test_app.py
══════════════════════════════════════════════════════════════════════════════
"""

import functools
import json
import os
import subprocess
import sys
from pathlib import Path

from anri.tools.registry import tool

SU_WINDOWS = sys.platform == "win32"

# Scorciatoie scritte a mano: nome detto dall'utente -> cosa passare ad apri().
# Servono per le app che il sistema non elenca o elenca con un nome diverso
# (su macOS i nomi delle app sono in inglese: "calcolatrice" -> Calculator).
if SU_WINDOWS:
    APP = {
        "calcolatrice": "calc.exe",
        "blocco note": "notepad.exe",
        "esplora file": "explorer.exe",
        "browser": "https://www.google.com",
    }
else:
    APP = {
        "calcolatrice": "/System/Applications/Calculator.app",
        "blocco note": "/System/Applications/TextEdit.app",
        "esplora file": "/System/Library/CoreServices/Finder.app",
        "impostazioni": "/System/Applications/System Settings.app",
        "browser": "https://www.google.com",
    }

# Cartelle dove macOS tiene le app (.app)
CARTELLE_APP_MAC = [
    Path("/Applications"),
    Path("/Applications/Utilities"),
    Path("/System/Applications"),
    Path("/System/Applications/Utilities"),
    Path.home() / "Applications",
]


def apri(destinazione: str) -> None:
    """Apre un programma, un file o un indirizzo web con il sistema operativo."""
    if SU_WINDOWS:
        os.startfile(destinazione)
    else:
        subprocess.run(["open", destinazione], check=True)


@functools.cache
def trova_app_installate() -> dict[str, str]:
    """Restituisce le app installate come {nome in minuscolo: cosa passare ad apri_app_installata}.

    Esempio su Windows: {"discord": "com.squirrel.Discord.Discord", ...}
    Esempio su macOS:   {"discord": "/Applications/Discord.app", ...}

    @functools.cache salva il risultato dopo la prima chiamata: interrogare
    il sistema richiede tempo, e le app installate non cambiano spesso.
    """
    app = _app_windows() if SU_WINDOWS else _app_mac()
    return {
        nome: app_id
        for nome, app_id in app.items()
        # scartiamo i programmi di disinstallazione, non vogliamo aprirli per sbaglio!
        if "uninstall" not in nome and "disinstalla" not in nome
    }


def _app_windows() -> dict[str, str]:
    """Chiede a Windows le app del menu Start."""
    comando = (
        "[Console]::OutputEncoding = [Text.Encoding]::UTF8; "
        "Get-StartApps | ConvertTo-Json -Compress"
    )
    risultato = subprocess.run(
        ["powershell", "-NoProfile", "-Command", comando],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return {app["Name"].lower(): app["AppID"] for app in json.loads(risultato.stdout)}


def _app_mac() -> dict[str, str]:
    """Cerca i pacchetti .app nelle cartelle delle applicazioni di macOS.

    Guarda anche un livello più in basso, perché alcune app stanno in una
    sottocartella (es. /Applications/Adobe Photoshop/Adobe Photoshop.app).
    """
    trovate: dict[str, str] = {}
    for cartella in CARTELLE_APP_MAC:
        if not cartella.is_dir():
            continue
        for percorso in [*cartella.glob("*.app"), *cartella.glob("*/*.app")]:
            # setdefault: se due cartelle hanno un'app con lo stesso nome, vince la prima
            trovate.setdefault(percorso.stem.lower(), str(percorso))
    return trovate


def apri_app_installata(app_id: str) -> None:
    """Apre un'app installata a partire da ciò che ha restituito trova_app_installate()."""
    if SU_WINDOWS:
        os.startfile(f"shell:AppsFolder\\{app_id}")
    else:
        apri(app_id)


@tool
def apri_app(nome: str) -> str:
    """Apre un'applicazione installata sul computer dell'utente.

    Args:
        nome: nome dell'applicazione da aprire, ad esempio "discord", "spotify" o "calcolatrice"
    """
    nome = nome.lower().strip()
    if nome in APP:
        apri(APP[nome])
        return f"Ho aperto {nome}."
    installata = trova_app_installate()
    if nome in installata:
        apri_app_installata(installata[nome])
        return f"Ho aperto {nome}."
    for nome_app, app_id in installata.items():
        if nome in nome_app:
            apri_app_installata(app_id)
            return f"Ho aperto {nome_app}."
    return f"Non ho trovato l'app {nome} sul computer."
