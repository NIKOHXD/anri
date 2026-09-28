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

from anri.tools.registry import tool

# Scorciatoie scritte a mano: nome detto dall'utente -> cosa passare a os.startfile.
# Servono per le app che Windows non elenca o elenca con un nome diverso.
APP = {
    "calcolatrice": "calc.exe",
    "blocco note": "notepad.exe",
    "esplora file": "explorer.exe",
    "browser": "https://www.google.com",
}


@functools.cache
def trova_app_installate() -> dict[str, str]:
    """Chiede a Windows le app del menu Start. Restituisce {nome in minuscolo: AppID}.

    Esempio: {"discord": "com.squirrel.Discord.Discord", "google chrome": "Chrome", ...}

    @functools.cache salva il risultato dopo la prima chiamata: interrogare
    Windows richiede circa un secondo, e le app installate non cambiano spesso.
    """
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
    return {
        app["Name"].lower(): app["AppID"]
        for app in json.loads(risultato.stdout)
        # scartiamo i programmi di disinstallazione, non vogliamo aprirli per sbaglio!
        if "uninstall" not in app["Name"].lower() and "disinstalla" not in app["Name"].lower()
    }


def apri_app_installata(app_id: str) -> None:
    """Apre un'app del menu Start a partire dal suo AppID."""
    os.startfile(f"shell:AppsFolder\\{app_id}")


@tool
def apri_app(nome: str) -> str:
    """Apre un'applicazione installata sul computer dell'utente.

    Args:
        nome: nome dell'applicazione da aprire, ad esempio "discord", "spotify" o "calcolatrice"
    """
    nome = nome.lower().strip()
    if nome in APP:
        os.startfile(APP[nome])

        return f"Ho aperto {nome}."
    installata = trova_app_installate()
    if nome in installata:
        apri_app_installata(installata[nome])
        return f"Ho aperto {nome}."
    for nome_app, app_id in installata.items():
        if nome in nome_app:
            apri_app_installata(app_id)
            return f"Ho aperto {nome}."
    return f"Non ho trovato l'app {nome} sul computer."
