# Main application file
import psycopg2
import psycopg2.extras
from flask import Flask, render_template

app = Flask(__name__)

# Database connection details
DB_HOST = "192.168.1.7"
DB_PORT = "5432"
DB_NAME = "sitdb"
DB_USER = "lizmap"
DB_PASS = "publ1sh"

def get_db_connection():
    """Establishes a connection to the database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

import sys

@app.route('/')
def index():
    """Mostra la tabella principale dei ponti."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT
                n_ponte, codice_iop, nome_ponte, comune, codice_istat,
                altri_comuni_confinanti, localita, tipo_sp, n_sp, nome_sp,
                progressiva_centro_km_m, progressiva_inizio_km_m, progressiva_fine_km_m
            FROM prv_vb_ponti_view
        """)
        ponti = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', ponti=ponti)
    except Exception as e:
        print(f"Errore in index: {e}", file=sys.stderr)
        return f"<h1>Errore di Database</h1><p>Impossibile recuperare i dati dei ponti. Dettagli: {e}</p>", 500

@app.route('/ponte/<n_ponte>')
def dettaglio_ponte(n_ponte):
    """Mostra i dettagli di un singolo ponte in una maschera con tab."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM prv_vb_ponti_view WHERE n_ponte = %s", (n_ponte,))
        ponte = cur.fetchone()
        cur.close()
        conn.close()

        if ponte is None:
            return "Ponte non trovato", 404

        return render_template('dettaglio_ponte.html', ponte=ponte)
    except Exception as e:
        print(f"Errore in dettaglio_ponte: {e}", file=sys.stderr)
        return f"<h1>Errore di Database</h1><p>Impossibile recuperare i dettagli del ponte. Dettagli: {e}</p>", 500

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible on the local network
    app.run(host='0.0.0.0', port=5001, debug=True)
