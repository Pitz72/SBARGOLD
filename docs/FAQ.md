# ❓ FAQ - Domande Frequenti su Sbargold

## Generale

### Cos'è Sbargold?
Sbargold è un linguaggio di programmazione esoterico ma completamente funzionante. È caratterizzato dall'uso di un solo comando base (`SBARGOLD`) declinato con simboli diversi per ottenere diverse funzionalità.

### È un linguaggio reale?
Sì! Sbargold è un linguaggio funzionante con un interprete Python. Puoi scrivere programmi veri che eseguono calcoli, manipolano dati e producono output.

### Qual è lo scopo di Sbargold?
Sbargold è stato creato come:
- Esperimento linguistico esoterico
- Strumento educativo per capire come funzionano gli interpreti
- Progetto divertente per esplorare design di linguaggi minimali

### Perché "Sbargold"?
Il nome combina unicità e l'idea di "oro" (gold), simboleggiando qualcosa di prezioso e distintivo nel mondo dei linguaggi di programmazione.

## Installazione e Setup

### Quali sono i requisiti?
- Python 3.6 o superiore
- Nessuna dipendenza esterna

### Come installo Sbargold?
1. Clona o scarica il repository
2. I file sono pronti all'uso, non serve installazione
3. Esegui: `python sbargold.py nome_file.sbg`

### Funziona su Linux/Mac/Windows?
Sì! Sbargold funziona su qualsiasi sistema con Python installato.

## Sintassi

### Perché tutti i comandi iniziano con SBARGOLD?
È la caratteristica distintiva del linguaggio. Ogni operazione è una "declinazione" del comando base, rendendo la sintassi unica e immediatamente riconoscibile.

### Posso abbreviare SBARGOLD?
No, l'interprete riconosce solo la forma completa `SBARGOLD` seguita dal simbolo appropriato.

### Case sensitive?
Sì, `SBARGOLD` deve essere scritto tutto in maiuscolo. `sbargold` o `Sbargold` non funzioneranno.

### Posso scrivere più comandi sulla stessa riga?
No, ogni comando deve stare su una riga separata.

## Programmazione

### Come faccio i commenti?
Usa `SBARGOLD#`:
```sbargold
SBARGOLD# Questo è un commento
```

### Come faccio un IF-ELSE?
Sbargold attualmente supporta solo IF. Per simulare un ELSE:
```sbargold
SBARGOLD# IF
SBARGOLD@ x > 5
SBARGOLD{
SBARGOLD! "x > 5"
SBARGOLD}

SBARGOLD# "ELSE" simulato
SBARGOLD@ x <= 5
SBARGOLD{
SBARGOLD! "x <= 5"
SBARGOLD}
```

### Come faccio un WHILE loop?
Non c'è un WHILE diretto. Usa `SBARGOLD~` con un contatore:
```sbargold
iterations SBARGOLD= 10
SBARGOLD~ iterations
SBARGOLD{
SBARGOLD# Codice del loop
SBARGOLD}
```

### Posso definire funzioni?
Attualmente no. È una delle limitazioni del linguaggio.

### Posso annidare i loop?
Sì:
```sbargold
SBARGOLD~ 3
SBARGOLD{
SBARGOLD! "Esterno"
SBARGOLD~ 2
SBARGOLD{
SBARGOLD! "Interno"
SBARGOLD}
SBARGOLD}
```

### Come gestisco le stringhe?
Le stringhe sono racchiuse tra doppi apici:
```sbargold
testo SBARGOLD= "Hello"
SBARGOLD! "World"
```

Nota: Attualmente non ci sono operazioni su stringhe (concatenazione, split, etc.)

### Posso fare operazioni matematiche complesse?
Le operazioni base sono: +, -, *, /

Per operazioni complesse, usa combinazioni:
```sbargold
SBARGOLD# Calcola (a + b) * c
temp SBARGOLD+ a b
risultato SBARGOLD* temp c
```

## Array

### Come creo un array?
```sbargold
nome_array SBARGOLD[] elemento1 elemento2 elemento3
```

### Posso modificare un elemento?
Attualmente no. Gli array sono immutabili dopo la creazione.

### Posso avere array multidimensionali?
No, gli array non possono contenere altri array.

### Come accedo a un elemento specifico?
Usa la notazione `array[indice]`:
```sbargold
primi SBARGOLD[] 2 3 5 7 11
primo_elemento SBARGOLD= primi[0]
```

## Errori Comuni

### "SBARGOLD ERROR: File non trovato"
Verifica:
- Il percorso del file è corretto
- Il file ha estensione `.sbg`
- Sei nella directory giusta

### Il programma non stampa nulla
Verifica:
- Hai usato `SBARGOLD!` per l'output
- La sintassi è corretta
- Non ci sono errori prima del comando print

### "Divisione per zero"
Aggiungi un controllo:
```sbargold
SBARGOLD@ divisore != 0
SBARGOLD{
risultato SBARGOLD/ dividendo divisore
SBARGOLD}
```

### I loop non funzionano
Verifica:
- Hai aperto con `SBARGOLD{`
- Hai chiuso con `SBARGOLD}`
- L'indentazione non conta, ma rende leggibile

## Confronto con Altri Linguaggi

### È simile a Python?
No, la sintassi è completamente diversa. L'interprete è scritto in Python, ma il linguaggio è unico.

### È come Brainfuck?
Sbargold è più leggibile. Brainfuck usa solo 8 caratteri incomprensibili, mentre Sbargold usa parole chiave con simboli.

### È Turing-completo?
Sì! Sbargold supporta:
- Variabili (memoria)
- Condizionali (decisioni)
- Loop (iterazione)

Questo lo rende Turing-completo.

## Sviluppo

### Posso contribuire?
Assolutamente! Puoi:
- Aggiungere nuove funzionalità all'interprete
- Creare nuovi esempi
- Migliorare la documentazione
- Segnalare bug

### Quali feature sono pianificate?
Possibili estensioni future:
- Funzioni definite dall'utente
- Operazioni su stringhe
- File I/O
- Dictionary/Map
- Moduli e import
- Debugger

### Come segnalo un bug?
Crea un issue con:
- Descrizione del problema
- Codice Sbargold che causa l'errore
- Output/errore ricevuto
- Comportamento atteso

### Posso usare Sbargold per progetti seri?
Sbargold è principalmente educativo e sperimentale. Per progetti reali, considera linguaggi mainstream come Python, JavaScript, etc.

## Prestazioni

### Sbargold è veloce?
No, è interpretato e non ottimizzato. Va bene per programmi piccoli ed educativi.

### Posso compilare Sbargold?
Attualmente no. Esiste solo un interprete Python.

### Ci sono limiti di dimensione del programma?
Solo i limiti della memoria del sistema. Ma programmi molto grandi saranno lenti.

## Curiosità

### Qual è il programma Sbargold più corto?
```sbargold
SBARGOLD! "!"
```

### Qual è il programma più lungo scritto in Sbargold?
Probabilmente `test_all.sbg` negli esempi!

### Posso scrivere un interprete Sbargold in Sbargold?
Tecnicamente possibile (è Turing-completo) ma sarebbe estremamente complesso e lento.

### Qualcuno usa davvero Sbargold?
È un linguaggio esoterico per divertimento ed educazione, non per uso produttivo!

---

**Non hai trovato risposta?** Crea un issue o contribuisci alla documentazione! 🏆✨
