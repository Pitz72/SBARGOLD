# 🗺️ Roadmap Evolutiva SBARGOLD

Il progetto **SBARGOLD** è passato da un semplice interprete sperimentale a un linguaggio esoterico robusto, sicuro e tecnicamente avanzato (v2.4.0). Ecco la visione per le evoluzioni future.

---

## 💎 Versione 3.0: Performance e Compilazione

L'obiettivo principale della prossima major release è il salto di prestazioni e l'indipendenza dall'interprete Python per l'esecuzione finale.

### 1. Architettura a Bytecode
*   Sostituire la valutazione diretta dell'AST con un **Compilatore di Bytecode**.
*   Sviluppare una **Virtual Machine (VM)** dedicata in C o Rust per eseguire il bytecode Sbargold a velocità nativa.

### 2. Compilazione Nativa (LLVM)
*   Esplorare l'uso di **LLVM** come backend per generare eseguibili binari nativi direttamente dal sorgente `.sbg`.

---

## 🛠️ Tooling e DX (Developer Experience)

Rendere la scrittura in Sbargold meno "esoterica" e più professionale.

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

## 📦 Linguaggio e Standard Library

Espandere le capacità espressive del linguaggio.

### 1. Gestione Errori Avanzata
*   Introdurre il comando `SBARGOLD!?` (Try-Catch) per permettere agli sviluppatori di gestire eccezioni a runtime senza interrompere il programma.

### 2. Standard Library (v3.0)
*   **`std:math`**: Funzioni trigonometriche, logaritmi e costanti.
*   **`std:io`**: Manipolazione avanzata di stream e socket di rete.
*   **`std:json`**: Supporto nativo per il parsing e la serializzazione JSON (mappato sui Dizionari Sbargold).

---

## 🌐 Ecosystem

### 1. SBARGOLD Web Playground
*   Compilare l'interprete/VM in **WebAssembly (WASM)** per permettere l'esecuzione di Sbargold direttamente nel browser senza installare Python.

### 2. Package Manager
*   Un semplice gestore di dipendenze per scaricare moduli Sbargold da repository remoti (es. GitHub).

---

**Sbargold** - _L'evoluzione dell'oro continua!_ 🏆✨
