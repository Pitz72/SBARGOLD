# 🚀 Quickstart - Sbargold

Benvenuto in **Sbargold**! Questa guida ti porterà da zero a scrivere il tuo primo programma in pochi minuti.

## ⚡ Setup Rapido

1. **Clona o scarica il repository**
2. **Verifica Python 3.6+**
   ```bash
   python --version
   ```
3. **Esegui il tuo primo programma**
   ```bash
   python sbargold.py examples/hello_world.sbg
   ```

## 📝 Il Tuo Primo Programma

Crea un file chiamato `primo.sbg` e scrivi:

```sbargold
SBARGOLD# Il mio primo programma Sbargold
SBARGOLD! "Ciao, sono il mio primo programma Sbargold!"

SBARGOLD# Fai una somma
eta SBARGOLD= 25
anni_futuri SBARGOLD= 10
eta_futura SBARGOLD+ eta anni_futuri

SBARGOLD! "Tra 10 anni avrai:"
SBARGOLD! eta_futura
```

Eseguilo:
```bash
python sbargold.py primo.sbg
```

## 🎯 Comandi Essenziali

### Output e Input
```sbargold
SBARGOLD! "Ciao!"      SBARGOLD# Stampa a video
nome SBARGOLD? "Nome:" SBARGOLD# Ricevi input (v2.0)
```

### Variabili e Matematica
```sbargold
x SBARGOLD= 100            SBARGOLD# Assegnazione
risultato SBARGOLD+ 5 3    SBARGOLD# Addizione
risultato SBARGOLD- 10 4   SBARGOLD# Sottrazione
risultato SBARGOLD* 6 7    SBARGOLD# Moltiplicazione
risultato SBARGOLD/ 20 4   SBARGOLD# Divisione
```

### Loop e Condizioni
```sbargold
SBARGOLD# Ripeti 5 volte
SBARGOLD~ 5 SBARGOLD{
    SBARGOLD! "Ciao!"
SBARGOLD}

SBARGOLD# Condizionale
x SBARGOLD= 10
SBARGOLD@ x > 5 SBARGOLD{
    SBARGOLD! "x è maggiore di 5"
SBARGOLD}
```

### Strutture Dati e Stringhe (v2.0)
```sbargold
SBARGOLD# Array
numeri SBARGOLD[] 1 2 3

SBARGOLD# Dizionario
utente SBARGOLD[:] "nome" "Mario" "età" 30
nome SBARGOLD. utente "nome"

SBARGOLD# Concatenazione Stringhe
saluto SBARGOLD& "Ciao " nome
```

## 🎮 Esegui gli Esempi

Usa gli script di utilità per un menu interattivo:

**Windows:**
```bash
run_examples.bat
```

**Linux/Mac:**
```bash
chmod +x run_examples.sh
./run_examples.sh
```

Oppure eseguili direttamente:
```bash
python sbargold.py examples/fibonacci.sbg
python sbargold.py examples/calculator.sbg
python sbargold.py examples/test_all.sbg
```

## 💡 Progetti Suggeriti per Iniziare

### 1. Contatore
```sbargold
SBARGOLD! "Conto fino a 10:"
i SBARGOLD= 1
SBARGOLD~ 10 SBARGOLD{
    SBARGOLD! i
    i SBARGOLD+ i 1
SBARGOLD}
```

### 2. Somma di una Lista
```sbargold
numeri SBARGOLD[] 10 20 30 40
totale SBARGOLD= 0
SBARGOLD~ n in numeri SBARGOLD{
    totale SBARGOLD+ totale n
SBARGOLD}
SBARGOLD! "Totale:"
SBARGOLD! totale
```

## 🎓 Cheat Sheet Rapido

| Comando | Descrizione |
|---|---|
| `SBARGOLD#` | Commento |
| `SBARGOLD!` | Stampa output |
| `SBARGOLD?` | Ricevi input |
| `SBARGOLD=` | Assegna variabile |
| `SBARGOLD+` | Addizione |
| `SBARGOLD-` | Sottrazione |
| `SBARGOLD*` | Moltiplicazione |
| `SBARGOLD/` | Divisione |
| `SBARGOLD@` | Se (condizione IF) |
| `SBARGOLD~` | Ripeti (Loop Count/Foreach) |
| `SBARGOLD[]` | Definisci Array |
| `SBARGOLD[:]` | Definisci Dizionario (v2.0) |
| `SBARGOLD&` | Concatena Stringhe (v2.0) |
| `SBARGOLD^` | Operazioni Stringhe (v2.0) |
| `SBARGOLD>>` | Scrittura File (v2.0) |
| `SBARGOLD<<` | Lettura File (v2.0) |
| `SBARGOLD{}` | Delimitatori Blocco |

## 🆘 Problemi Comuni

**L'interprete non parte?**
Verifica di essere nella directory giusta e che Python sia installato.

**Errori di sintassi?**
- Tutti i comandi devono iniziare con `SBARGOLD` in maiuscolo.
- Le stringhe usano doppi apici `"testo"`.
- I blocchi si aprono con `SBARGOLD{` e chiudono con `SBARGOLD}`.

## 🎯 Prossimi Passi
1. Leggi la [Documentazione Completa](DOCUMENTATION.md) per i dettagli.
2. Esplora le specifiche formali in [grammar.ebnf](grammar.ebnf).
3. Esegui la suite di test con `python tests/run_tests.py` (v2.0+).
