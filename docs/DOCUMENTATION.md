# 📚 Documentazione SBARGOLD 24K.LINGOTTO-1

> **Nota sul Versionamento**: SBARGOLD utilizza la Scala di Purezza dell'Oro:
> - **24K** (99.9%): Oro puro - Rilascio stabile
> - **22K** (91.7%): Feature-complete
> - **18K** (75%): Core solido
> - **14K** (58.3%): MVP
> - **9K** (37.5%): Prototipo

## Indice
1. [Introduzione](#introduzione)
2. [Sintassi Base](#sintassi-base)
3. [Variabili e Tipi](#variabili-e-tipi)
4. [Input/Output](#inputoutput)
5. [Scope e Closures](#scope-e-closures)
6. [Strutture di Controllo](#strutture-di-controllo)
7. [Funzioni](#funzioni)
8. [Stringhe (v2.0)](#stringhe-v20)
9. [File I/O (v2.0)](#file-io-v20)
10. [Strutture Dati (v2.0)](#strutture-dati-v20)
11. [Moduli (v2.0)](#moduli-v20)
12. [Debug](#debug)

## Introduzione
SBARGOLD è un linguaggio esoterico dove ogni comando inizia con la parola chiave `SBARGOLD`.
La 24K.LINGOTTO-1 introduce la precedenza degli operatori (PEMDAS) e la protezione degli import.

## Sintassi Base
Ogni istruzione deve iniziare con un comando SBARGOLD.
```sbargold
SBARGOLD! "Hello World"  SBARGOLD# Stampa a video
```

### Espressioni, Matematica e Logica (PEMDAS)
Il linguaggio supporta operazioni matematiche e logiche tramite notazione infix, rispettando l'ordine di precedenza PEMDAS (Parentesi, Esponenti, Moltiplicazione, Divisione, Addizione, Sottrazione) esteso alla logica booleana.
- **Aritmetica**: `+`, `-`, `*`, `/`
- **Confronto**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logica (v24K.LINGOTTO-6)**: `AND`, `OR`, prefisso `NOT`
- **Raggruppamento (v24K.LINGOTTO-6)**: Le parentesi tonde `()` forzano la precedenza.

**Esempio di Logica Booleana:**
```sbargold
SBARGOLD@ (x > 10) AND (NOT (y == 5)) SBARGOLD{
    SBARGOLD! "Condizione complessa verificata!"
SBARGOLD}
```

## Variabili e Tipi
Assegnazione:
```sbargold
x SBARGOLD= 10
name SBARGOLD= "Mario"
```

### Mutazione Avanzata (L-Values)
SBARGOLD permette di modificare strutture dati esistenti (Dizionari e Array) usando la **dot-notation** o l'espressione di accesso.
```sbargold
user SBARGOLD[:] "name" "Mario" "age" 30
user.name SBARGOLD= "Luigi"  SBARGOLD# Modifica una chiave
user.age SBARGOLD= 31

list SBARGOLD[] 10 20 30
list.0 SBARGOLD= 99 SBARGOLD# Modifica un indice (col punto)
```
> **Nota**: Gli identificatori dopo il punto (es. `user.name`) sono trattati automaticamente come stringhe. Per l'accesso dinamico, usare il comando `SBARGOLD. obj chiave`.

## Input/Output
Stampa a video:
```sbargold
SBARGOLD! "Messaggio"
SBARGOLD! variabile
```

Input utente:
```sbargold
nome SBARGOLD? "Inserisci il tuo nome: "
```

## Scope e Closures
SBARGOLD supporta lo **scope lessicale**. Le funzioni catturano l'ambiente in cui sono definite.

> **⚠️ NOTA IMPORTANTE (24K.LINGOTTO-3)**: Le closures catturano le **variabili**, non i **valori**.
> Se una variabile captured viene modificata dopo la definizione della funzione, il closure vedrà il nuovo valore.
> Questo è il comportamento standard (come JavaScript/Python), ma può essere sorprendente.

```sbargold
SBARGOLD# Esempio di Closure
SBARGOLD> crea_contatore x SBARGOLD{
    SBARGOLD> inc SBARGOLD{
        x SBARGOLD+ x 1
        SBARGOLD< x
    SBARGOLD}
    SBARGOLD< inc
SBARGOLD}
```

**Esempio di Capture by Reference (attenzione!):**
```sbargold
valore SBARGOLD= 10

SBARGOLD> get_valore SBARGOLD{
    SBARGOLD< valore  # Cattura la variabile 'valore', non il valore 10
SBARGOLD}

SBARGOLD! get_valore    # Stampa: 10
valore SBARGOLD= 99     # Modifica la variabile catturata
SBARGOLD! get_valore    # Stampa: 99 (non 10!)
```

**Soluzione: Passa per valore se necessario:**
```sbargold
valore SBARGOLD= 10
snapshot SBARGOLD= valore  # Cattura il valore attuale

SBARGOLD> get_snapshot SBARGOLD{
    SBARGOLD< snapshot  # Ora è sicuro, 'snapshot' non cambia più
SBARGOLD}
```

## Strutture di Controllo
Le strutture di controllo permettono di gestire il flusso di esecuzione del programma.

### Condizionali (IF / ELSE IF / ELSE)
SBARGOLD supporta strutture condizionali a catena:
```sbargold
SBARGOLD@ x > 20 SBARGOLD{
    SBARGOLD! "Grande"
SBARGOLD}
SBARGOLD@? x > 10 SBARGOLD{
    SBARGOLD! "Medio"
SBARGOLD}
SBARGOLD@! SBARGOLD{
    SBARGOLD! "Piccolo"
SBARGOLD}
```

### Ciclo WHILE (Ciclo Condizionale)
Esegue un blocco finché la condizione è vera:
```sbargold
count SBARGOLD= 0
SBARGOLD~~ count < 10 SBARGOLD{
    SBARGOLD! count
    count SBARGOLD+ count 1
SBARGOLD}
```

### Ciclo LOOP (Iterazione)
Supporta due modalità: conteggio e foreach.
Loop (Count):
```sbargold
SBARGOLD~ 5 SBARGOLD{
    SBARGOLD! "Ripeto..."
SBARGOLD}
```
Loop (Foreach):
```sbargold
SBARGOLD~ item in array SBARGOLD{
    SBARGOLD! item
SBARGOLD}
```

## Funzioni
Definizione:
```sbargold
SBARGOLD> somma a b SBARGOLD{
    res SBARGOLD+ a b
    SBARGOLD< res
SBARGOLD}
```
Chiamata:
```sbargold
risultato SBARGOLD$ somma 5 10
```

## Stringhe (22K)
Concatenazione:
```sbargold
full SBARGOLD& str1 str2
```

## File I/O (22K)
Scrittura (Sandboxed 22K.BULLIONE-2):
```sbargold
SBARGOLD>> "file.txt" "contenuto"
```
Lettura:
```sbargold
contenuto SBARGOLD<< "file.txt"
```

## Strutture Dati
### Array (v24K.LINGOTTO-6)
Gli array sono espressioni di prima classe e possono essere nidificati:
```sbargold
matrice SBARGOLD[] (SBARGOLD[] 1 2) (SBARGOLD[] 3 4)
SBARGOLD! matrice.0.1  SBARGOLD# Stampa 2
```

### Dizionari (22K)
Definizione:
```sbargold
user SBARGOLD[:] "name" "Mario" "age" 30
```
Accesso dinamico:
```sbargold
name SBARGOLD. user "name"
```

## Moduli (22K)
Importazione (24K.LINGOTTO-1 con protezione ciclica):
```sbargold
SBARGOLD| "libs/math.sbg"
```

## Debug
Eseguire con flag `-d`:
`python sbargold.py -d script.sbg`
