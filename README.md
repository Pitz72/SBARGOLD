# 🏆 SBARGOLD - Il Linguaggio Esoterico dell'Oro (v2.4.0)

**Sbargold** è un linguaggio di programmazione esoterico, fittizio ma completamente funzionante, basato sulla filosofia del "Monovocabolo": un singolo comando, **SBARGOLD**, declinato in varie modalità attraverso simboli per ottenere diverse funzionalità.

## 📋 Caratteristiche (v2.4.0)

- ✨ **Un solo comando**: Tutto ruota attorno a SBARGOLD
- 🎯 **Motore Moderno**: Basato su Lexer, Parser e AST (v2.4 con PEMDAS)
- 🚀 **Turing-completo**: Supporta variabili, array, loop, condizionali e funzioni
- 🔐 **Closures**: Supporto nativo per lo scope lessicale e le chiusure (v2.3.0)
- 🛡️ **Sicurezza**: Sandbox File System, Watchdog e Protezione Import Circolari (v2.4.0)
- 📦 **Modulare**: Supporto per importazione moduli (`SBARGOLD|`)
- 🗂️ **Strutture Dati**: Dizionari (`SBARGOLD[:]`) e Array (`SBARGOLD[]`)
- 📄 **File I/O**: Lettura e scrittura file (`SBARGOLD>>`, `SBARGOLD<<`)
- 🔤 **String Ops**: Manipolazione avanzata stringhe (`SBARGOLD&`, `SBARGOLD^`)
- 🛠️ **Dev Tools**: Debugger CLI integrato (`-d`) e Estensione VS Code

## 🧭 Indice della Documentazione (Table of Contents)

Tutta la documentazione è stata centralizzata per una navigazione più chiara.

### 🚀 Per Iniziare
* **[Quickstart / Guida Rapida](docs/QUICKSTART.md)**: Il punto di partenza ideale per scrivere il tuo primo codice.

### 📚 Documentazione Tecnica
* **[Documentazione Completa](docs/DOCUMENTATION.md)**: Tutti i comandi e la sintassi nel dettaglio.
* **[Grammatica Formale (EBNF)](docs/grammar.ebnf)**: Specifiche tecniche della sintassi del linguaggio.
* **[Project Overview](docs/PROJECT_OVERVIEW.md)**: Panoramica dell'architettura e degli scopi educativi.

### 🔧 Sviluppo e Community
* **[Changelog Storico](docs/CHANGELOG.md)**: Storico delle versioni (fino alla v2.1.0).
* **[FAQ](docs/FAQ.md)**: Domande frequenti.
* **[Contribuire (Contributing)](docs/CONTRIBUTING.md)**: Linee guida per sviluppare il core o aggiungere esempi.
* **[Analisi Critica](docs/ANALISI_CRITICA_SBARGOLD.md)**: Un'analisi sullo stato del linguaggio pre-v2.0.

## ⚡ Esecuzione Rapida

Assicurati di avere Python 3.6+ installato. Esegui i file `.sbg` con l'interprete:

```bash
# Esecuzione standard
python sbargold.py examples/hello_world.sbg

# Modalità Debugger
python sbargold.py -d examples/loop.sbg
```

### Script Menu (Interattivi)
- **Windows**: `run_examples.bat`
- **Linux/Mac**: `./run_examples.sh`

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT come esperimento educativo e linguaggio esoterico.
Vedi il file [LICENSE](LICENSE) per i dettagli.

---

**Sbargold** - _Dove l'oro si trasforma in codice!_ 🏆✨
