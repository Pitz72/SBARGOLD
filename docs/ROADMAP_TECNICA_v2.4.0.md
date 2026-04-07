# 🗺️ Roadmap Evoluzione Linguaggio SBARGOLD (v24K.LINGOTTO-6)

Questa roadmap dettaglia i passaggi per trasformare SBARGOLD da un linguaggio esoterico di base a un linguaggio di programmazione strutturato e resiliente, mantenendo la filosofia del monovocabolo.

## 🏁 Step 1: Espressività e Logica [COMPLETATO]
- [x] **Logica Booleana**: Operatori `AND`, `OR`, `NOT`.
- [x] **Short-circuiting**: Ottimizzazione della valutazione logica nell'Interpreter.
- [x] **Raggruppamento**: Supporto per le parentesi tonde `()` per gestire le precedenze PEMDAS.
- [x] **Test & Docs**: Creato `tests/test_logic.py` e aggiornata la documentazione base.

## 🚀 Step 2: Strutture di Controllo Avanzate [COMPLETATO]
- [x] **ELSE IF (`SBARGOLD@?`)**: Permettere catene di condizioni multiple.
- [x] **ELSE (`SBARGOLD@!`)**: Blocco di fallback se nessuna condizione `IF` o `ELIF` è vera.
- [x] **WHILE Loop (`SBARGOLD~~`)**: Iterazione basata su una condizione dinamica (es. `SBARGOLD~~ x < 100`).
- [x] **Integrazione AST**: Refactoring di `IfStatement` e creazione di `WhileStatement`.
- [x] **Test**: Creato `tests/test_control_flow.py`.

## 🛠️ Step 3: Mutazione e Riferimenti (L-Values) [COMPLETATO]
- [x] **Assegnazione Profonda**: Supporto per modificare elementi di array e chiavi di dizionari (es. `user.name SBARGOLD= "Nuovo"`).
- [x] **Refactoring Interpreter**: Risoluzione dei riferimenti invece dei soli valori durante l'assegnazione.
- [x] **Dot Notation**: Supporto per l'operatore `.` infix con zucchero sintattico per gli identificatori.
- [x] **Array as Expression**: `SBARGOLD[]` promosso a espressione nidificabile.

## 🛡️ Step 4: Resilienza (Try-Catch) [IN CORSO]
- [ ] **TRY (`SBARGOLD!?`) / CATCH (`SBARGOLD!!`)**: Gestione degli errori a runtime.
- [ ] **Variabile di Errore**: Cattura del messaggio di errore in una variabile SBARGOLD per l'ispezione nel blocco catch.

## 💎 Step 5: Tipizzazione e Casting
- [ ] **CAST (`SBARGOLD::`)**: Conversione esplicita tra tipi (`INT`, `FLOAT`, `STR`, `BOOL`).
- [ ] **Validazione Rigorosa**: Sollevamento di errori catturabili in caso di cast falliti.

---
*Ultimo aggiornamento: 2026-04-07*
