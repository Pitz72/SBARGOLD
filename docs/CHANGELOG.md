# 📝 Changelog - Sbargold

Tutti i cambiamenti significativi del progetto sono documentati in questo file.

## 🏆 Sistema di Versionamento: Scala di Purezza dell'Oro

SBARGOLD utilizza un sistema di versionamento esoterico basato sulla scala di purezza dell'oro:

| Versione | Purezza | Significato |
|----------|---------|-------------|
| **24K** | 99.9% | Oro puro - Rilascio stabile, completo, pronto per produzione |
| **22K** | 91.7% | Feature-complete, testing finale |
| **18K** | 75% | Core solido, feature in consolidamento |
| **14K** | 58.3% | MVP funzionante, API non stabili |
| **9K** | 37.5% | Prototipo, proof-of-concept |

**Schema**: `SBARGOLD-{KARATI}.{EDIZIONE}` es: `24K.LINGOTTO-1`, `22K.BULLIONE`

---

## 24K.LINGOTTO-7 (Oro Puro - Parser & Test Suite Hardening)
*Data: 2026-05-21*
*Precedente: 24K.LINGOTTO-6*

### 🔧 Fix & Stabilità
- **Parser Retrocompatibilità**: Aggiunto supporto nel Parser (`sbargold_core/parser.py`) per interpretare i comandi funzionali (`SBARGOLD&`, `SBARGOLD^`, `SBARGOLD<<` e `SBARGOLD.`) come istruzioni di assegnamento tradizionale a sinistra, permettendo l'esecuzione di script legacy senza causare `SyntaxError`.
- **Suite di Test Hardening**: Corretto l'assertion error nel test del parser (`test_parser.py`) in cui il formato testuale atteso non rispecchiava la rappresentazione `Var(x)` dei nodi identificatori dell'AST.
- **Tasso di Successo del 100%**: Ripristinato il tasso di successo del **100%** su tutti i 13 test del linguaggio.

---

## 24K.LINGOTTO-6 (Step 1 - Espressività e Logica)
*Data: In sviluppo*
*Precedente: 24K.LINGOTTO-5*

### ✨ Evoluzione Architetturale
- **Logica Booleana**: Introdotti gli operatori `AND`, `OR` e `NOT` come parole chiave native. Integrati nel Lexer e nel Parser PEMDAS (Livelli 5 e 6).
- **Short-circuiting**: L'interprete ora valuta le espressioni logiche con la tecnica di "corto circuito" (salta la seconda condizione se non necessaria), migliorando prestazioni e sicurezza.
- **Raggruppamento Espressioni**: Aggiunto supporto per le parentesi tonde `()` nel Lexer e Parser per forzare la priorità in espressioni complesse matematiche o logiche.
- **Flusso di Controllo (v24K.LINGOTTO-6 Step 2)**:
    - **SBARGOLD@? (ELSE IF)**: Supporto per rami condizionali multipli.
    - **SBARGOLD@! (ELSE)**: Aggiunta del blocco di fallback per la struttura `IF`.
    - **SBARGOLD~~ (WHILE)**: Implementazione del ciclo condizionale dinamico (Turing-completezza espressiva).

---

## 24K.LINGOTTO-6 (Oro Puro - Logica & Mutazione)
*Data: 2026-04-07*
*Precedente: 24K.LINGOTTO-5*

### ✨ Evoluzione Architetturale
- **Logica Booleana**: Introdotti operatori infix `AND`, `OR` e prefisso `NOT`. Supporto per raggruppamento tramite parentesi `()`.
- **Mutazione Strutture Dati (L-Values)**: Il comando `SBARGOLD=` ora supporta obiettivi complessi (es. `user.age SBARGOLD= 31`). Implementata risoluzione dei riferimenti nell'Interpreter.
- **Espressioni di Prima Classe**: Promosso `SBARGOLD[]` (Array) a espressione nidificabile. Refactoring PEMDAS con Livello 0 (Dot Access).
- **Controllo del Flusso Avanzato**: Implementati `SBARGOLD@?` (ELSE IF), `SBARGOLD@!` (ELSE) e `SBARGOLD~~` (WHILE Loop condizionale).

### 🔧 Fix & Stabilità
- **Lexer Precision**: Corretto il bug del punto decimale nei numeri float che interferiva con l'operatore di accesso proprietà.
- **Terminator Logic v2**: Implementato lookahead profondo per identificare catene di assegnazione nidificate e prevenire il consumo errato di argomenti.
- **Zucchero Sintattico**: Gli identificatori dopo il punto (es. `obj.prop`) vengono ora trattati come stringhe letterali, eliminando la necessità di virgolette per accessi statici.

---

## 24K.LINGOTTO-5 (Oro Puro - Stability & Isolation)
*Data: 2026-04-07*
*Precedente: 24K.LINGOTTO-4*

### ✨ Evoluzione Architetturale
- **SBARGOLD-Expressions**: I comandi funzionali (`&`, `^`, `<<`, `.`, `$`) sono stati promossi a espressioni di prima classe. Ora possono essere nidificati liberamente, es: `SBARGOLD! SBARGOLD& "Hello " SBARGOLD^ "UPPER" name`.
- **Namespace `:`**: Supporto nativo per i namespace negli identificatori. L'importazione di moduli ora isola automaticamente le funzioni e i globali, rendendoli accessibili tramite il prefisso `nome_file:membro`.
- **Isolamento Moduli**: Ogni comando `SBARGOLD|` (Import) crea un'istanza dedicata dell'interprete, garantendo uno scope di esecuzione protetto e indipendente.

### 🔧 Fix & Stabilità
- **Terminator Logic**: Ottimizzato il parser per distinguere correttamente tra argomenti di una lista e l'inizio di un nuovo statement di assegnazione (Lookahead 1 su IDENTIFIER).
- **Encoding Universale**: Rimossi caratteri non-ASCII dalla test suite per garantire la compatibilità totale su ambienti Windows (fix UnicodeEncodeError).
- **Recursion Sync**: Sincronizzato `sys.setrecursionlimit` di Python con il `MAX_CALL_DEPTH` di SBARGOLD per prevenire crash grezzi dell'host.
- **Parser Robustness**: Rafforzato il tracciamento `in_function` per impedire l'uso di `SBARGOLD<` (Return) nel corpo principale dello script.

---

## 24K.LINGOTTO-4 (Oro Puro - Robustness & UX)
*Data: 2026-04-07*
*Precedente: 24K.LINGOTTO-3*

### 🔧 Risolte 5 Criticità MEDIE

#### 9. Input Type Coercion Fragile
- **Problema**: Input "007" → 7 (confusione octal), "3.14.15" → stringa "3.14.15" (comportamento inconsistente)
- **Soluzione**: Parser input robusto con validazione esplicita. Int puri (solo cifre), float (un separatore), altrimenti stringa.

#### 10. Array Index Float
- **Problema**: `arr[1.9]` accedeva a `arr[1]` tramite casting implicito. Indici negativi non gestiti correttamente.
- **Soluzione**: Validazione rigorosa - indice deve essere intero puro (`is_integer()` check). Bounds check esplicito con messaggi chiari.

#### 11. String Op Case-Sensitive Confusione
- **Problema**: Documentazione non chiara su case-sensitivity. "len" vs "LEN" potenzialmente confusi.
- **Soluzione**: Confermato case-insensitive (LEN/len/LeN tutti validi). Messaggio errore aggiornato con lista operazioni valide.

#### 12. Debugger Non Testabile
- **Problema**: Dipendenza hardcoded da `sys.stdin.isatty()` e `input()`, difficile da mockare nei test.
- **Soluzione**: Refactor `_debug_step()` con dependency injection - accetta `input_func` e `output_func` opzionali.

#### 13. Parser Recovery Assente
- **Problema**: Token sconosciuti venivano skippati silenziosamente (`self._consume(); return None`), permettendo parsing parziale.
- **Soluzione**: Errore esplicito `SyntaxError` con dettagli su token, valore, linea e colonna.

### ✨ Miglioramenti UX
- Messaggi errore più descrittivi per indici array e operazioni stringa
- Debugger testabile con mock input/output
- Fail-fast parsing per errori sintassi

---

## 24K.LINGOTTO-3 (Oro Puro - Parser & Language Fixes)
*Data: 2026-04-07*
*Precedente: 24K.LINGOTTO-2*

### 🔧 Risolte 4 Criticità GRAVI

#### 5. Parser PEMDAS Incompleto
- **Problema**: Il parser aveva codice morto per `OP_ADD`/`OP_SUB` che non esistevano nel lexer. Espressioni infix come `a + b * c` non erano supportate.
- **Soluzione**: Aggiunti token `OP_ADD`, `OP_SUB`, `OP_MUL`, `OP_DIV` al lexer. Implementati `_parse_addition()` e `_parse_multiplication()` completi nel parser.

#### 6. Lexer Ignora Caratteri Sconosciuti
- **Problema**: `_read_operator()` saltava silenziosamente caratteri non riconosciuti (`self.pos += 1`), causando errori di sintassi mascherati e comportamenti imprevedibili.
- **Soluzione**: Genera `SyntaxError` esplicito con dettagli su carattere, linea, colonna e ASCII code.

#### 7. Global State - Funzioni Sovrascrivono Senza Warning
- **Problema**: Definire una funzione con nome esistente sovrascriveva silenziosamente la precedente (last-write-wins).
- **Soluzione**: Aggiunto `RuntimeWarning` quando una funzione sovrascrive un'altra, con indicazione della linea della definizione precedente.

#### 8. Closure Capture Comportamento Sorprendente
- **Problema**: Le closures catturano variabili per riferimento, non per valore. Modifiche post-definizione affectano il closure (comportamento corretto ma sorprendente).
- **Soluzione**: Documentazione aggiornata in `DOCUMENTATION.md` con esempio chiaro del comportamento e workaround (snapshot pattern).

### ✨ Miglioramenti
- Supporto completo espressioni infix con precedenza operatori (PEMDAS)
- Errori di lexer più informativi
- Warning per redefinizione funzioni
- Documentazione closures con esempi pratici

---

## 24K.LINGOTTO-2 (Oro Puro - Security Hardening)
*Data: 2026-04-07*
*Precedente: 24K.LINGOTTO-1*

### 🛡️ Risolte 4 Criticità GRAVISSIME

#### 1. Path Traversal Bypass (Sandbox Escape)
- **Problema**: `_safe_path()` usava `startswith()` che falliva con path normalizzati (`../`, symlink).
- **Soluzione**: Implementato `os.path.realpath()` per risolvere symlink e normalizzare path. Aggiunto check con separatore per prevenire match parziali.

#### 2. Race Condition TOCTOU (Import/Read)
- **Problema**: `os.path.exists()` seguito da `open()` creava finestra temporale per attacco symlink swap.
- **Soluzione**: Eliminato pre-check. Ora apertura atomica con gestione `FileNotFoundError` e `PermissionError`.

#### 3. Exception Handling Silente
- **Problema**: `except Exception` wrappava tutto in `RuntimeError`, perdendo traceback originale.
- **Soluzione**: Preservazione traceback completo con `traceback.format_exc()` e `raise ... from e`.

#### 4. DoS Watchdog Inefficace
- **Problema**: `MAX_INSTRUCTIONS` contava statement AST, non operazioni reali. Loop semplici eseguivano milioni di operazioni senza triggerare il limit.
- **Soluzione**: Sostituito con `MAX_OPERATIONS` (100,000) che conta operazioni effettive: iterazioni loop, I/O, operazioni aritmetiche, elementi array/dict.

### 🔒 Miglioramenti Security
- Conteggio granulari operazioni negli hotpath (loop, I/O, strutture dati)
- Costi diversificati: I/O (5 ops), Import (50 ops), iterazioni (1 op ciascuna)
- Messaggi errore dettagliati con path risolto per debugging

---

## 24K.LINGOTTO-1 (Oro Puro - PEMDAS & Module Security)
*Data: 2026-03-17*
*Precedente: 22K.BULLIONE-3*

### ✨ Ottimizzazioni Core
- **Precedenza Operatori**: Implementato il sistema PEMDAS nel Parser per calcoli matematici corretti.
- **Protezione Import**: Aggiunto rilevamento e blocco automatico degli import circolari.
- **AST Detailing**: Migliorata la rappresentazione testuale dei nodi AST per il debugging.

### 📚 Documentazione
- Aggiunte docstrings a tutto il codice sorgente (`sbargold_core/`).
- Introdotto sistema di versionamento "Purezza dell'Oro".

---

## 22K.BULLIONE-3 (Closures & Lexer Hardening)
*Data: 2026-03-17*
*Precedente: 22K.BULLIONE-2*

### ✨ Aggiunte Logiche
- **Supporto Closures**: Le funzioni ora supportano lo scope lessicale. È possibile definire funzioni che "catturano" le variabili locali dello scope superiore.
- **Lexer Robusto**: Migliorata la validazione dei comandi `SBARGOLD`. Comandi malformati ora generano errori di sintassi chiari invece di comportamenti imprevedibili.

---

## 22K.BULLIONE-2 (Security & Core Hardening)
*Data: 2026-03-17*
*Precedente: 22K.BULLIONE-1*

### 🛡️ Sicurezza (Risolte Criticità Gravissime)
- **Sandbox File System**: Introdotto blocco anti Path Traversal. I comandi `SBARGOLD>>` (Write), `SBARGOLD<<` (Read) e `SBARGOLD|` (Import) non possono più accedere a file al di fuori della root del progetto di esecuzione.
- **Protezione Denial of Service (DoS)**: Implementati `MAX_CALL_DEPTH` (limite di ricorsione: 1000) e `MAX_INSTRUCTIONS` (limite esecuzioni: 5.000.000) per prevenire crash del sistema host causati da stack overflow o loop infiniti malformati.

---

## 22K.BULLIONE-1 (Rilascio Core 2.0)
*Data: 2025-12-05*
*Precedente: 18K.LAMINA*

### ✨ Aggiunte e Ristrutturazioni Core
- **Core Refactoring**: L'interprete è stato diviso in moduli all'interno di `sbargold_core/`. Ora è basato su **Lexer**, **Parser** e valutazione **AST**, abbandonando la fragile esecuzione riga per riga della v1.x.
- **Gestione Errori Robusta**: Implementato stack trace per errori, permettendo un debugging reale del codice.
- **Operazioni su Stringhe**: Aggiunto `SBARGOLD&` per la concatenazione e `SBARGOLD^` per manipolazioni come `LEN`, `UPPER`, `SPLIT`.
- **Strutture Dati Avanzate**: Aggiunto supporto ai Dizionari tramite `SBARGOLD[:]` e accesso alle chiavi tramite `SBARGOLD.`.
- **File I/O**: Introdotti i comandi `SBARGOLD>>` (Scrittura) e `SBARGOLD<<` (Lettura) per l'interazione col file system.
- **Modularità**: Introdotta l'importazione di altri script via `SBARGOLD|`.
- **Debugger CLI**: Supporto nativo integrato con il flag `-d` (`python sbargold.py -d ...`) per il tracing riga per riga.

### 🛠️ Ecosistema e Qualità
- Aggiunta una definizione formale del linguaggio in `docs/grammar.ebnf`.
- Nuova suite di test completa (`tests/run_tests.py`).
- Rilasciata un'estensione base per il Syntax Highlighting in VS Code (`vscode_extension/`).

---

## 18K.LAMINA (Supporto Funzioni)
*Data: 2025-11-01*
*Precedente: 14K.GRANELLO*

### ✨ Aggiunte
- **Supporto per Funzioni Utente**:
  - Aggiunto il comando `SBARGOLD>` per definire funzioni.
  - Aggiunto il comando `SBARGOLD$` per chiamare funzioni.
  - Aggiunto il comando `SBARGOLD<` per ritornare valori.
  - Implementato uno scope di variabili locale per le funzioni.
- **Esempi**: Aggiunti `functions.sbg` e `text_adventure.sbg`.

---

## 14K.GRANELLO (Rilascio Iniziale)
*Data: 2025-10-01*

- Rilascio iniziale del linguaggio Sbargold.
- Interprete Python "naïve" funzionante (parsing line-by-line).
- Set di comandi base (variabili, I/O, aritmetica, loop, condizionali, array).
- Documentazione e file di esempio base.

---

## [Unreleased / Roadmap Futura]

### � Prossima Release Target: 24K.LINGOTTO-2
- Fix criticità sicurezza Path Traversal
- Compilatore (da sorgente `.sbg` a binario nativo).
- REPL interattivo dedicato.
- Supporto a chiamate asincrone e Network (HTTP).
- Meccanismo di `Try-Catch` per gestione errori gestita dall'utente.

---

**Sbargold** - _La purezza dell'oro nel codice!_ 🏆✨
