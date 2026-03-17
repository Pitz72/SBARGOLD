# Piano di Risoluzione Criticità Medie/Leggere e Aggiornamento v2.4.0

## 🎯 Obiettivo
Risolvere le problematiche rimanenti: implementare la **precedenza degli operatori** (PEMDAS), prevenire **import circolari** (infinite recursion), migliorare la **rappresentazione AST** e aggiungere la **documentazione interna** (docstrings). Aggiornare la versione a **2.4.0**.

## 🛠️ Azioni Proposte (Piano di Esecuzione)

### Fase 1: Precedenza Operatori (`sbargold_core/parser.py`)
*   Ristrutturare il parsing delle espressioni in livelli gerarchici:
    1.  `_parse_expression` (Entry point)
    2.  `_parse_comparison` (`==`, `!=`, `<`, `>`, `<=`, `>=`)
    3.  `_parse_addition` (`+`, `-`)
    4.  `_parse_multiplication` (`*`, `/`)
    5.  `_parse_term` (Numeri, Stringhe, Identificatori, Chiamate)

### Fase 2: Protezione Import Circolari (`sbargold_core/interpreter.py`)
*   Aggiungere `self.import_stack` all'oggetto `Interpreter`.
*   Prima di eseguire un `SBARGOLD|`, verificare se il file è già presente nello stack di importazione corrente. In caso positivo, sollevare un `RuntimeError` per prevenire il crash per memoria esaurita.

### Fase 3: Qualità del Codice e AST (`sbargold_core/ast.py`, `lexer.py`, `interpreter.py`)
*   Aggiornare i metodi `__repr__` in `ast.py` per includere tutti i dati rilevanti (es. valori assegnati, condizioni, ecc.).
*   Aggiungere docstrings standard alle classi e ai metodi principali per facilitare la manutenzione futura.

### Fase 4: Aggiornamento Versione e Documentazione Finale
*   Aggiornare `README.md`, `docs/DOCUMENTATION.md` e `docs/CHANGELOG.md` alla versione **2.4.0**.
*   Creare `docs/logs/2.4.0.md` con il riepilogo tecnico dell'ottimizzazione dell'interprete.

## ✅ Risultato Atteso
Un linguaggio maturo con calcoli matematici corretti (precedenza), un sistema di moduli sicuro contro i loop infiniti e un codice sorgente professionale e auto-esplicativo.
