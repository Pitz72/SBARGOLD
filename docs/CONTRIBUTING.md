# 🤝 Contribuire a Sbargold

Grazie per l'interesse nel contribuire al progetto Sbargold! Ogni contributo è benvenuto.

## 🌟 Modi per Contribuire

### 1. 📝 Segnalare Bug
Se trovi un bug:
1. Verifica che non sia già stato segnalato
2. Crea un issue con:
   - Descrizione chiara del problema
   - Codice Sbargold che riproduce il bug
   - Output atteso vs output ricevuto
   - Versione Python usata

### 2. 💡 Proporre Nuove Funzionalità
Per suggerire una nuova feature:
1. Crea un issue con etichetta "enhancement"
2. Descrivi la funzionalità desiderata
3. Spiega il caso d'uso
4. Proponi la sintassi (opzionale)

### 3. 🔨 Contribuire Codice
Per contribuire codice:

#### Setup
```bash
git clone https://github.com/yourusername/SBARGOLD.git
cd SBARGOLD
```

#### Workflow
1. **Crea un branch**
   ```bash
   git checkout -b feature/nome-feature
   ```

2. **Fai le modifiche**
   - Segui lo stile del codice esistente
   - Aggiungi test se appropriato
   - Aggiorna la documentazione

3. **Testa le modifiche**
   ```bash
   python sbargold.py examples/test_all.sbg
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "Descrizione chiara della modifica"
   ```

5. **Push e Pull Request**
   ```bash
   git push origin feature/nome-feature
   ```
   Poi crea una Pull Request su GitHub

### 4. 📚 Migliorare la Documentazione
La documentazione può sempre essere migliorata:
- Correzioni grammaticali/ortografiche
- Chiarimenti
- Nuovi esempi
- Traduzioni

### 5. 🎨 Creare Esempi
Contribuisci con nuovi programmi di esempio:
1. Crea un file `.sbg` in `examples/`
2. Usa commenti per spiegare il codice
3. Testa che funzioni
4. Aggiorna il README con il nuovo esempio

## 📋 Linee Guida

### Stile Codice Python
- Segui PEP 8
- Usa nomi descrittivi per variabili e funzioni
- Aggiungi docstring per funzioni pubbliche
- Mantieni le funzioni focalizzate e brevi

### Stile Codice Sbargold
- Usa commenti (`SBARGOLD#`) per spiegare la logica
- Nomi di variabili descrittivi
- Organizza il codice in sezioni logiche
- Aggiungi una descrizione all'inizio del file

### Commit Messages
Usa messaggi chiari e descrittivi:
- ✅ "Aggiunto supporto per operazioni su stringhe"
- ✅ "Fix: Gestione corretta di array vuoti"
- ✅ "Docs: Aggiunto esempio di ricorsione"
- ❌ "fix stuff"
- ❌ "update"

## 🎯 Aree di Sviluppo Prioritarie

### Alta Priorità
- [ ] Funzioni definite dall'utente
- [ ] Gestione errori più robusta
- [ ] Operazioni su stringhe (concatenazione, substring, etc.)
- [ ] File I/O (lettura/scrittura file)

### Media Priorità
- [ ] Dictionary/Map
- [ ] Operazioni matematiche avanzate (potenza, radice, etc.)
- [ ] Debugging tools
- [ ] Syntax highlighting per editor

### Bassa Priorità
- [ ] Moduli e import
- [ ] Compilatore (da interprete a eseguibile)
- [ ] REPL interattivo
- [ ] Package manager

## 🧪 Testing

Quando aggiungi nuove funzionalità:
1. Crea un esempio in `examples/`
2. Testa con casi limite
3. Verifica che `test_all.sbg` funzioni ancora
4. Aggiungi test specifici se necessario

## 📖 Documentazione

Quando modifichi il codice, aggiorna:
- `README.md` - Panoramica
- `DOCUMENTATION.md` - Dettagli tecnici
- `QUICKSTART.md` - Guide rapide (se rilevante)
- `FAQ.md` - Domande comuni (se rilevante)

## ✅ Checklist Pull Request

Prima di inviare una PR, verifica:
- [ ] Il codice funziona e passa tutti i test
- [ ] Hai aggiunto test per nuove funzionalità
- [ ] La documentazione è aggiornata
- [ ] I commit sono puliti e ben descritti
- [ ] Non ci sono file non necessari (cache, temp, etc.)
- [ ] Il codice segue lo stile del progetto

## 🎓 Risorse per Contribuire

### Imparare Python
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

### Interpreti e Linguaggi
- [Crafting Interpreters](https://craftinginterpreters.com/)
- [Build Your Own Lisp](http://www.buildyourownlisp.com/)

### Git e GitHub
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 💬 Comunità

- Sii rispettoso e costruttivo
- Aiuta altri contributor
- Condividi conoscenza e esperienze
- Divertiti! 🎉

## 🏆 Riconoscimenti

Tutti i contributor saranno riconosciuti nel README del progetto.

---

**Grazie per contribuire a Sbargold!** 🌟✨
