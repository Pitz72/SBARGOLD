# 🗺️ Roadmap Evolutiva SBARGOLD

Il progetto **SBARGOLD** è passato da un semplice interprete sperimentale a un linguaggio esoterico robusto, sicuro e tecnicamente avanzato (**24K.LINGOTTO-6**). Ecco la visione per le evoluzioni future.

## 🏆 Sistema di Versionamento: Scala di Purezza dell'Oro

| Versione | Purezza | Fase | Descrizione |
|----------|---------|------|-------------|
| **24K** | 99.9% | Produzione | Oro puro - Rilascio stabile e completo |
| **22K** | 91.7% | Release Candidate | Feature-complete, testing finale |
| **18K** | 75% | Beta | Core solido, feature in consolidamento |
| **14K** | 58.3% | Alfa | MVP funzionante, API non stabili |
| **9K** | 37.5% | Prototipo | Proof-of-concept |

---

## 💎 24K.LINGOTTO-2: Performance e Compilazione

L'obiettivo principale della prossima major release 24K è il salto di prestazioni e l'indipendenza dall'interprete Python per l'esecuzione finale.

### 1. Architettura a Bytecode
*   Sostituire la valutazione diretta dell'AST con un **Compilatore di Bytecode**.
*   Sviluppare una **Virtual Machine (VM)** dedicata in C o Rust per eseguire il bytecode Sbargold a velocità nativa.

### 2. Compilazione Nativa (LLVM)
*   Esplorare l'uso di **LLVM** come backend per generare eseguibili binari nativi direttamente dal sorgente `.sbg`.

---

## 🛠️ 22K.BULLIONE-4: Tooling e DX (Developer Experience)

Rendere la scrittura in Sbargold meno "esoterica" e più professionale. Target: raggiungere 24K.

### 1. LSP (Language Server Protocol)
*   Sviluppare un server LSP per fornire:
    *   Autocompletamento intelligente.
    *   Go-to-definition per funzioni e variabili.
    *   Linting in tempo reale (segnalazione errori prima dell'esecuzione).

### 2. REPL Dedicato
*   Creare una shell interattiva avanzata con:
    *   History dei comandi.
    *   Syntax highlighting in-terminal.
    *   Ispezione live dello stato della memoria.

---

## 📦 18K+ : Linguaggio e Standard Library

Espandere le capacità espressive del linguaggio per avanzare verso 22K.

### 1. Gestione Errori Avanzata
*   Introdurre il comando `SBARGOLD!?` (Try-Catch) per permettere agli sviluppatori di gestire eccezioni a runtime senza interrompere il programma.

### 2. Standard Library (Target 22K → 24K)
*   **`std:math`**: Funzioni trigonometriche, logaritmi e costanti.
*   **`std:io`**: Manipolazione avanzata di stream e socket di rete.
*   **`std:json`**: Supporto nativo per il parsing e la serializzazione JSON (mappato sui Dizionari Sbargold).

---

## 🌐 Ecosystem (Target 24K.LINGOTTO-3+)

### 1. SBARGOLD Web Playground
*   Compilare l'interprete/VM in **WebAssembly (WASM)** per permettere l'esecuzione di Sbargold direttamente nel browser senza installare Python.

### 2. Package Manager
*   Un semplice gestore di dipendenze per scaricare moduli Sbargold da repository remoti (es. GitHub).

---

**Sbargold** - _L'evoluzione dell'oro continua!_ 🏆✨
