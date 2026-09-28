"""Gli strumenti che Anri può usare per agire sul computer e nel mondo.

Per aggiungere un nuovo strumento:
1. crea (o apri) un file in questa cartella
2. scrivi una funzione con tipi e docstring chiari, decorata con @tool
3. importa il modulo qui sotto, altrimenti il decoratore non viene mai eseguito
"""

# Importare i moduli fa eseguire i loro @tool, che riempiono il registro.
from anri.tools import app, meteo, tempo, timer  # noqa: F401
from anri.tools.registry import TOOLS, esegui

__all__ = ["TOOLS", "esegui"]
