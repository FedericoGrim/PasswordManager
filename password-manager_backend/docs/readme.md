# Generazione Documentazione - Password Manager Backend

Per generare la documentazione automatica del codice Python con Sphinx:

---

## 1. Preparazione

- Assicurarsi che **ogni cartella contenente file `.py` abbia un file `__init__.py`** (anche vuoto).  
- Scrivere **docstring** (cioè spiegazioni delle funzioni) tra `''' ... '''` o `""" ... """`, subito dopo la definizione di funzioni, classi e metodi.

---

## 2. Generazione dei file `.rst`

Aprire il terminale, spostarsi nella cartella `docs`, ed eseguire il comando:

    sphinx-apidoc -o . ../

Questo comando genererà file `.rst` (uno per modulo) partendo dai commenti nei file `.py`.  
Serviranno per creare automaticamente la documentazione.

---

## 3. Lancio della pagina di documentazione

- Spostare i file `.rst` generati dentro la cartella `docs/source/`.
- Aggiungere `modules.rst` (o il file principale generato) all'interno del file `index.rst`, sotto la direttiva `.. toctree::`, così:

    .. toctree::
       :maxdepth: 2
       :caption: Indice

       modules

- Spostarsi nella cartella `docs/source` ed eseguire il comando:

    sphinx-autobuild . _build/html

Ora la pagina web della documentazione sarà accessibile all'indirizzo:

    http://127.0.0.1:8000

e si aggiornerà automaticamente ad ogni modifica al codice o ai commenti.