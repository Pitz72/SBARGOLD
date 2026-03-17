# 📚 Documentazione SBARGOLD v2.4.0

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
La v2.4 introduce la precedenza degli operatori (PEMDAS) e la protezione degli import.

## Sintassi Base
Ogni istruzione deve iniziare con un comando SBARGOLD.
```sbargold
SBARGOLD! "Hello World"  SBARGOLD# Stampa a video
```

## Variabili e Tipi
Assegnazione:
```sbargold
x SBARGOLD= 10
name SBARGOLD= "Mario"
```

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

## Strutture di Controllo
If:
```sbargold
SBARGOLD@ x > 5 SBARGOLD{
    SBARGOLD! "Maggiore di 5"
SBARGOLD}
```

Loop (Count):
```sbargold
SBARGOLD~ 5 SBARGOLD{
    SBARGOLD! "Ripeto..."
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

## Stringhe (v2.0)
Concatenazione:
```sbargold
full SBARGOLD& str1 str2
```

## File I/O (v2.0)
Scrittura (Sandboxed v2.2):
```sbargold
SBARGOLD>> "file.txt" "contenuto"
```
Lettura:
```sbargold
contenuto SBARGOLD<< "file.txt"
```

## Strutture Dati (v2.0)
Dizionari:
```sbargold
user SBARGOLD[:] "name" "Mario" "age" 30
```
Accesso:
```sbargold
name SBARGOLD. user "name"
```

## Moduli (v2.0)
Importazione (v2.4 con protezione ciclica):
```sbargold
SBARGOLD| "libs/math.sbg"
```

## Debug
Eseguire con flag `-d`:
`python sbargold.py -d script.sbg`
