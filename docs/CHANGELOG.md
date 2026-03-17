# 📝 Changelog - Sbargold

Tutti i cambiamenti significativi del progetto sono documentati in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Versione 2.4.0 (PEMDAS & Module Security)
*Data: 2026-03-17*

### ✨ Ottimizzazioni Core
- **Precedenza Operatori**: Implementato il sistema PEMDAS nel Parser per calcoli matematici corretti.
- **Protezione Import**: Aggiunto rilevamento e blocco automatico degli import circolari.
- **AST Detailing**: Migliorata la rappresentazione testuale dei nodi AST per il debugging.

### 📚 Documentazione
- Aggiunte docstrings a tutto il codice sorgente (`sbargold_core/`).

---

## Versione 2.3.0 (Closures & Lexer Hardening)
*Data: 2026-03-17*

### ✨ Aggiunte Logiche
- **Supporto Closures**: Le funzioni ora supportano lo scope lessicale. È possibile definire funzioni che "catturano" le variabili locali dello scope superiore.
- **Lexer Robusto**: Migliorata la validazione dei comandi `SBARGOLD`. Comandi malformati ora generano errori di sintassi chiari invece di comportamenti imprevedibili.

---

## Versione 2.2.0 (Security & Core Hardening Update)
*Data: 2026-03-17*

### 🛡️ Sicurezza (Risolte Criticità Gravissime)
- **Sandbox File System**: Introdotto blocco anti Path Traversal. I comandi `SBARGOLD>>` (Write), `SBARGOLD<<` (Read) e `SBARGOLD|` (Import) non possono più accedere a file al di fuori della root del progetto di esecuzione.
- **Protezione Denial of Service (DoS)**: Implementati `MAX_CALL_DEPTH` (limite di ricorsione: 1000) e `MAX_INSTRUCTIONS` (limite esecuzioni: 5.000.000) per prevenire crash del sistema host causati da stack overflow o loop infiniti malformati.

---

## Versione 2.1.0 (Rilascio SBARGOLD 2.0)
*Data: 2025-12-05*

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

## Versione 1.1.0 (01/11/2025)

### ✨ Aggiunte
- **Supporto per Funzioni Utente**:
  - Aggiunto il comando `SBARGOLD>` per definire funzioni.
  - Aggiunto il comando `SBARGOLD$` per chiamare funzioni.
  - Aggiunto il comando `SBARGOLD<` per ritornare valori.
  - Implementato uno scope di variabili locale per le funzioni.
- **Esempi**: Aggiunti `functions.sbg` e `text_adventure.sbg`.

---

## Versione 1.0.0

- Rilascio iniziale del linguaggio Sbargold.
- Interprete Python "naïve" funzionante (parsing line-by-line).
- Set di comandi base (variabili, I/O, aritmetica, loop, condizionali, array).
- Documentazione e file di esempio base.

---

## [Unreleased / Roadmap Futura]

### 💡 Proposte Future
- Compilatore (da sorgente `.sbg` a binario nativo).
- REPL interattivo dedicato.
- Supporto a chiamate asincrone e Network (HTTP).
- Meccanismo di `Try-Catch` per gestione errori gestita dall'utente.

---

**Sbargold** - _Tracking Excellence!_ 🏆✨
