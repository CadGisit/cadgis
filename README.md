# Visualizzatore Dati Ponti

Questa è una semplice applicazione web realizzata con Flask per visualizzare i dati dei ponti da un database PostgreSQL con estensione PostGIS. L'applicazione è stata progettata per essere utilizzata all'interno di una rete locale.

## Funzionalità

- **Pagina Principale**: Una tabella che mostra un elenco di tutti i ponti, con funzionalità di ricerca e ordinamento per ogni colonna.
- **Pagina di Dettaglio**: Cliccando su un ponte nella tabella, si accede a una pagina di dettaglio con informazioni complete suddivise in tab per argomento.
- **Integrazione Mappe**: I tab "Inquadramento" e "StreetView" mostrano le viste di Google Maps e StreetView corrispondenti alla posizione del ponte.

## Prerequisiti

- Python 3.x
- `pip` per l'installazione delle dipendenze

## Installazione

1.  **Clona o Scarica il Codice**:
    Assicurati di avere tutti i file (`app.py`, `requirements.txt`, la cartella `templates`, etc.) in una stessa directory sul computer da cui eseguirai l'applicazione.

2.  **Crea un Ambiente Virtuale (Consigliato)**:
    Apri un terminale o un prompt dei comandi nella directory del progetto e esegui:
    ```bash
    python -m venv venv
    ```
    Attiva l'ambiente virtuale:
    - Su Windows: `venv\Scripts\activate`
    - Su macOS/Linux: `source venv/bin/activate`

3.  **Installa le Dipendenze**:
    Con l'ambiente virtuale attivo, installa le librerie necessarie eseguendo:
    ```bash
    pip install -r requirements.txt
    ```

## Configurazione

Le impostazioni per la connessione al database si trovano all'inizio del file `app.py`. Se le credenziali o l'indirizzo del database dovessero cambiare, modifica queste righe:

```python
# Database connection details
DB_HOST = "192.168.1.7"
DB_PORT = "5432"
DB_NAME = "sitdb"
DB_USER = "lizmap"
DB_PASS = "publ1sh"
```

## Esecuzione

1.  **Avvia l'Applicazione**:
    Assicurati che il tuo terminale sia nella directory del progetto e che l'ambiente virtuale (se creato) sia attivo. Esegui il seguente comando:
    ```bash
    python app.py
    ```

2.  **Accedi all'Applicazione**:
    Apri un browser web e vai all'indirizzo:
    `http://127.0.0.1:5001`

    Se stai eseguendo l'applicazione su un server e vuoi accedervi da un altro computer nella stessa rete, usa l'indirizzo IP del server invece di `127.0.0.1`. Ad esempio: `http://192.168.1.100:5001` (sostituendo `192.168.1.100` con l'IP reale del computer su cui gira l'applicazione).

## Note sulle Foto

Il tab "Foto" nella pagina di dettaglio mostra i percorsi dei file delle immagini come memorizzati nel database. Per visualizzare effettivamente le immagini, è necessario che questi percorsi siano URL accessibili dal browser. Se sono percorsi di file locali sul server, sarebbe necessario implementare una route aggiuntiva in Flask per "servire" queste immagini. La logica attuale non include questa funzionalità.
