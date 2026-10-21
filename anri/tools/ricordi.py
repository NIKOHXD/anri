"""Strumenti: ricordare e dimenticare fatti sull'utente (Fase 5).

═══════════════════════════ ESERCIZIO 4 (medio) ════════════════════════════
La parte che legge e scrive il file è già pronta in anri/memoria.py:
    memoria.carica()        -> list[str]   i fatti salvati
    memoria.salva(fatti)                   sovrascrive il file con la nuova lista
Tu devi scrivere i due strumenti che l'LLM userà.

`ricorda(fatto)`:
  1. togli gli spazi all'inizio e alla fine del fatto
  2. se il fatto è vuoto, restituisci una stringa che contiene "vuoto"
     (senza salvare niente)
  3. se il fatto è già in memoria (ignorando maiuscole e minuscole),
     restituisci "Lo sapevo già." (senza salvarlo due volte)
  4. altrimenti aggiungilo in fondo alla lista, salva, e restituisci
     "Ok, me lo ricorderò."

`dimentica(argomento)`:
  1. elimina TUTTI i fatti che contengono `argomento`
     (ignorando maiuscole e minuscole: "pizza" toglie anche "Ama la Pizza")
  2. se non ne hai eliminato nessuno, restituisci
     "Non ricordavo niente su <argomento>."
  3. altrimenti salva i fatti rimasti e restituisci
     "Ho dimenticato: <fatto1>; <fatto2>."  (i fatti eliminati, separati da "; ")

Suggerimenti:
  - "Ciao".lower() == "ciao"
  - una list comprehension con if filtra una lista:
      [x for x in lista if condizione(x)]
  - "; ".join(["a", "b"]) == "a; b"

Verifica:  python -m pytest tests/test_ricordi.py
Poi provalo davvero:  python main.py  ->  "ricordati che studio informatica",
chiudi, riapri e chiedi "cosa studio?". Con /memoria vedi cosa ha salvato.
══════════════════════════════════════════════════════════════════════════════
"""

from anri import memoria
from anri.tools.registry import tool


@tool
def ricorda(fatto: str) -> str:
    """Salva un fatto importante sull'utente, per ricordarlo nelle prossime conversazioni.

    Usalo quando l'utente ti chiede di ricordare qualcosa, o ti dice qualcosa di
    personale che vale la pena sapere anche in futuro (nome, studi, gusti, abitudini).

    Args:
        fatto: il fatto da ricordare, scritto in terza persona, ad esempio "Studia informatica"
    """
    fatto = fatto.strip()
    if fatto == "":
        return "il fatto è vuoto"
    else:
        fatti_salvati = memoria.carica()
        if fatto.lower() in [f.lower() for f in fatti_salvati]:
            return "Lo sapevo già."
        else:
            fatti_salvati.append(fatto)
            memoria.salva(fatti_salvati)
            return "Ok, me lo ricorderò."


@tool
def dimentica(argomento: str) -> str:
    """Cancella dalla memoria i fatti sull'utente che riguardano un certo argomento.

    Usalo quando l'utente ti chiede di dimenticare qualcosa o dice che un fatto non è più vero.

    Args:
        argomento: parola chiave dei fatti da cancellare, ad esempio "pizza" o "università"
    """
    argomento = argomento.strip()
    if argomento == "":
        # "" è contenuto in qualsiasi stringa: senza questo controllo cancellerebbe tutto
        return "L'argomento da dimenticare è vuoto."
    fatti_salvati = memoria.carica()
    fatti_da_dimenticare = [fatto for fatto in fatti_salvati if argomento.lower() in fatto.lower()]
    if not fatti_da_dimenticare:
        return f"Non ricordavo niente su {argomento}."
    else:
        fatti_rimasti = [fatto for fatto in fatti_salvati if argomento.lower() not in fatto.lower()]
        memoria.salva(fatti_rimasti)
        return f"Ho dimenticato: {'; '.join(fatti_da_dimenticare)}."
