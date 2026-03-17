# Piano di Risoluzione Criticità Gravi e Aggiornamento v2.3.0

## 🎯 Obiettivo
Risolvere le problematiche di natura logica e sintattica classificate come "Gravi": la mancanza di supporto per le **Closures** (Lexical Scoping) e la fragilità del **Lexer** nel riconoscimento dei comandi. Aggiornare la versione a **2.3.0**.

## 🟠 Problemi da Risolvere
1.  **Mancanza di Closures**: Attualmente le funzioni hanno accesso solo allo scope globale. Definire funzioni all'interno di altre funzioni o loop non permette di "catturare" le variabili locali circostanti.
2.  **Fragilità del Lexer**: Il Lexer consuma i 8 caratteri di `SBARGOLD` e poi tenta di leggere il suffisso, ma non valida correttamente se il comando è atomico o se ci sono caratteri spuri attaccati (es. `SBARGOLDXYZ` viene interpretato parzialmente).

## 🛠️ Azioni Proposte (Piano di Esecuzione)

### Fase 1: Implementazione Closures (`sbargold_core/interpreter.py`)
*   **Classe `Function`**: Introdurre una classe interna o una struttura per memorizzare sia il nodo AST della funzione sia l'ambiente (`Environment`) attivo al momento della definizione.
*   **`_execute` (FunctionDefStatement)**: Quando una funzione viene definita, salvarla nel dizionario `self.functions` insieme al `self.environment` corrente (lo scope di chiusura).
*   **`_call_function`**: Quando la funzione viene chiamata, il nuovo ambiente (`func_env`) dovrà avere come genitore lo scope di chiusura catturato, non più forzatamente `self.globals`.

### Fase 2: Rafforzamento del Lexer (`sbargold_core/lexer.py`)
*   **Tokenizzazione Atomica**: Modificare `_read_command` per verificare che il comando `SBARGOLD` sia seguito immediatamente da un suffisso valido.
*   **Gestione Errori**: Se la sequenza inizia con `SBARGOLD` ma non corrisponde a nessun comando conosciuto (es. `SBARGOLD!!!`), sollevare un `SyntaxError` immediato invece di produrre token generici o ignorare il problema.

### Fase 3: Aggiornamento Versione e Documentazione
*   Aggiornare `README.md`, `docs/DOCUMENTATION.md` e `docs/CHANGELOG.md` alla versione **2.3.0**.
*   Documentare il supporto ufficiale alle **Closures** e al **Lexical Scoping**.
*   Creare `docs/logs/2.3.0.md` con i dettagli tecnici della ristrutturazione dello scope.

## ✅ Risultato Atteso
Un linguaggio più potente che supporta paradigmi di programmazione avanzati (funzioni di ordine superiore, closures) e un parser più resiliente agli errori di battitura nei comandi.
