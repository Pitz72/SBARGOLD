# 🏆 Sbargold - Project Overview

## 📁 Struttura del Progetto

```
SBARGOLD/
│
├── 📄 sbargold.py              # Interprete principale
│
├── 📚 Documentazione
│   ├── README.md               # Panoramica del progetto
│   ├── DOCUMENTATION.md        # Documentazione completa
│   ├── QUICKSTART.md          # Guida rapida per iniziare
│   ├── FAQ.md                 # Domande frequenti
│   ├── CONTRIBUTING.md        # Guida per contribuire
│   ├── LICENSE                # Licenza MIT
│   └── PROJECT_OVERVIEW.md    # Questo file
│
├── 📂 examples/               # Programmi di esempio
│   ├── hello_world.sbg        # Hello World classico
│   ├── calculator.sbg         # Calcolatrice completa
│   ├── loop.sbg              # Esempio di loop
│   ├── conditional.sbg        # Esempio di condizionali
│   ├── arrays.sbg            # Gestione array
│   ├── fibonacci.sbg         # Sequenza di Fibonacci
│   ├── factorial.sbg         # Calcolo fattoriale
│   ├── test_all.sbg          # Test completo di tutte le feature
│   └── text_adventure.sbg    # Gioco testuale di avventura
│
├── 🚀 Script di Esecuzione
│   ├── run_examples.bat       # Menu interattivo (Windows)
│   └── run_examples.sh        # Menu interattivo (Linux/Mac)
│
└── ⚙️ Configurazione
    └── .gitignore             # File da ignorare in Git
```

## 🎯 Componenti Principali

### 1. Interprete (`sbargold.py`)
- **Classe principale**: `SbargoldInterpreter`
- **Funzionalità**:
  - Parser di sintassi Sbargold
  - Esecutore di comandi
  - Gestione variabili e array
  - Valutatore di espressioni
  - Gestione strutture di controllo

### 2. Comandi del Linguaggio

| Simbolo | Comando | Funzione |
|---------|---------|----------|
| `#` | Commento | Annotazioni nel codice |
| `!` | Output | Stampa a schermo |
| `?` | Input | Riceve input utente |
| `=` | Assegnazione | Assegna valore a variabile |
| `+` | Addizione | Somma due valori |
| `-` | Sottrazione | Sottrae due valori |
| `*` | Moltiplicazione | Moltiplica due valori |
| `/` | Divisione | Divide due valori |
| `@` | Condizionale | Esegue se condizione vera |
| `~` | Loop | Ripete blocco di codice |
| `[]` | Array | Crea/gestisce array |
| `{}` | Blocco | Delimita blocchi di codice |
| `>` | Definizione Funzione | Definisce una funzione utente |
| `<` | Ritorno Valore | Ritorna un valore da una funzione |
| `$` | Chiamata Funzione | Chiama una funzione utente |

### 3. Tipi di Dati Supportati
- **Numeri**: Interi e float
- **Stringhe**: Testo tra doppi apici
- **Array**: Liste di elementi

### 4. Operatori di Confronto
- `==` uguale
- `!=` diverso
- `<` minore
- `>` maggiore
- `<=` minore o uguale
- `>=` maggiore o uguale

## 🎓 Esempi Educativi

### Complessità Crescente

1. **Principiante** (`hello_world.sbg`)
   - Output base
   - Primo approccio al linguaggio

2. **Base** (`calculator.sbg`, `loop.sbg`)
   - Variabili
   - Operazioni aritmetiche
   - Loop semplici

3. **Intermedio** (`conditional.sbg`, `arrays.sbg`)
   - Condizionali
   - Gestione array
   - Iterazione su collezioni

4. **Avanzato** (`fibonacci.sbg`, `factorial.sbg`)
   - Algoritmi classici
   - Combinazione di strutture
   - Logica complessa

5. **Esperto** (`test_all.sbg`, `text_adventure.sbg`)
   - Test completo
   - Applicazioni interattive
   - Tutte le funzionalità

## 🔧 Come Usare

### Esecuzione Diretta
```bash
python sbargold.py programma.sbg
```

### Esecuzione Inline
```bash
python sbargold.py -c 'SBARGOLD! "Ciao!"'
```

### Menu Interattivo
**Windows:**
```bash
run_examples.bat
```

**Linux/Mac:**
```bash
chmod +x run_examples.sh
./run_examples.sh
```

## 📊 Statistiche del Progetto

- **Linee di codice interprete**: ~400
- **Esempi inclusi**: 8
- **Comandi del linguaggio**: 12
- **Pagine di documentazione**: 6
- **Estensione file**: `.sbg`

## 🌟 Caratteristiche Uniche

### 1. Minimalismo Radicale
Un solo comando base (`SBARGOLD`) per tutto.

### 2. Sintassi Visuale
I simboli rendono immediatamente chiaro il tipo di operazione.

### 3. Leggibilità
Nonostante l'unicità, il codice rimane leggibile:
```sbargold
SBARGOLD# Calcola area rettangolo
base SBARGOLD= 5
altezza SBARGOLD= 3
area SBARGOLD* base altezza
SBARGOLD! area
```

### 4. Completezza
Nonostante la semplicità, è Turing-completo.

## 🚀 Possibili Estensioni Future

### Implementate
- [x] **Funzioni**: `SBARGOLD>` per definire, `SBARGOLD$` per chiamare, `SBARGOLD<` per ritornare.

### Priorità Alta
- [ ] **Stringhe**: Operazioni di concatenazione e manipolazione
- [ ] **File I/O**: `SBARGOLD>>` e `SBARGOLD<<` per file

### Priorità Media
- [ ] **Dictionary**: `SBARGOLD{}` con sintassi key-value
- [ ] **Try-Catch**: `SBARGOLD!?` per gestione errori
- [ ] **Import**: `SBARGOLD^` per moduli
- [ ] **Math**: Funzioni matematiche avanzate

### Priorità Bassa
- [ ] **OOP**: Classi e oggetti
- [ ] **Async**: Programmazione asincrona
- [ ] **Network**: Richieste HTTP
- [ ] **GUI**: Interfacce grafiche

## 🎯 Obiettivi del Progetto

### Educativi
- Insegnare come funzionano gli interpreti
- Esplorare design di linguaggi minimali
- Praticare parsing e valutazione di espressioni

### Creativi
- Creare un linguaggio unico e riconoscibile
- Sfidare le convenzioni dei linguaggi tradizionali
- Dimostrare che "meno è più"

### Pratici
- Fornire un interprete funzionante
- Includere esempi pratici
- Documentazione completa

## 📖 Risorse per Approfondire

### Interpreti
- **Crafting Interpreters** di Bob Nystrom
- **Writing An Interpreter In Go** di Thorsten Ball

### Linguaggi Esoterici
- **Brainfuck**: Il più famoso linguaggio esoterico
- **Whitespace**: Usa solo spazi, tab e newline
- **Shakespeare**: Codice che sembra prosa

### Design di Linguaggi
- **SICP** (Structure and Interpretation of Computer Programs)
- **The Art of the Interpreter**

## 🤝 Contribuire

Sbargold è open source! Contribuisci:
- Migliorando l'interprete
- Aggiungendo esempi
- Scrivendo documentazione
- Segnalando bug
- Proponendo feature

Vedi `CONTRIBUTING.md` per dettagli.

## 📜 Licenza

Rilasciato sotto licenza MIT. Vedi `LICENSE` per dettagli.

## 🎉 Credits

Sbargold è nato come esperimento linguistico ed educativo.

**Versione**: 1.0.0  
**Anno**: 2024  
**Linguaggio Implementazione**: Python 3  
**Tipo**: Linguaggio esoterico Turing-completo

---

## 🔗 Quick Links

- **Start**: `QUICKSTART.md`
- **Docs**: `DOCUMENTATION.md`
- **FAQ**: `FAQ.md`
- **Examples**: `examples/`
- **Contribute**: `CONTRIBUTING.md`

---

**Sbargold** - _Un linguaggio, infinite possibilità!_ 🏆✨
