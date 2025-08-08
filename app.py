# Main application file
import psycopg2
import psycopg2.extras
from flask import Flask, render_template

app = Flask(__name__)

# Database connection details
DB_HOST = "192.168.1.1"
DB_PORT = "5432"
DB_NAME = "xnomedatabasex"
DB_USER = "xnomeutentex"
DB_PASS = "xpasswordutentex"

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

@app.route('/ponte/<int:n_ponte>')
def dettaglio_ponte(n_ponte):
    """Mostra i dettagli di un singolo ponte in una maschera con tab."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Explicitly list all columns to avoid issues with problematic data types from SELECT *
        query = """
            SELECT
                n_ponte, codice_iop, nome_ponte, comune, codice_istat, altri_comuni_confinanti,
                localita, tipo_sp, n_sp, nome_sp, progressiva_centro_km_m,
                progressiva_inizio_km_m, progressiva_fine_km_m, coord_x_epsg4326_centro,
                coord_y_epsg4326_centro, quota_centro, classificazione, tipo_collegamento,
                tipo_attraversamento, n_carreggiate, n_corsie, luce_estesa_inferiore_6_metri,
                luce_estesa, luce_campata_max, lungh_totale, largh_carreggiata,
                largh_fuori_tutto, n_campate, tracciato_ponte, tipologia_strutturale,
                tipologia_strutturale_voce_altro, tipologia_spalla_iniziale,
                tipologia_spalla_finale, pile_materiale_costruttivo,
                pile_materiale_costruttivo_voce_altro, pile_altezza_m, pile_geometria_sezione,
                pile_n_fondazioni, impalcato_materiale_costruttivo,
                impalcato_materiale_costruttivo_voce_altro, impalcato_tipologia_soletta,
                impalcato_tipologia_soletta_voce_altro, classificazione_uso_stradale,
                distretto, proprietario, classificazione_sismica_2025,
                sismicita_area_ag_g_tr475, classi_conseguenza, prp_2004,
                psda_rischio_idraulico, pai_rischio_frane, n_ispezioni_effettuate,
                data_ultima_ispezione, stato_opera, fenomeni_erosivi, fenomeni_franosi,
                morfologia_sito, tipologia_giunti, n_totale_giunti, lungh_giunto_spalla,
                lungh_giunto_pila, apparecchi_di_appoggio, interventi_strutturali_eseguiti,
                descrizione_interventi_strutturali, limitazione_di_carico, foto_path_lizmap,
                foto_path, link_google_maps, link_streetview
            FROM prv_vb_ponti_view WHERE n_ponte = %s
        """
        cur.execute(query, (n_ponte,))
        ponte = cur.fetchone()
        cur.close()
        conn.close()

        if ponte is None:
            return "Ponte non trovato", 404

        return render_template('dettaglio_ponte.html', ponte=ponte)
    except Exception as e:
        # Return a more detailed error message for debugging
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"ERRORE DIAGNOSTICO in dettaglio_ponte: Tipo={error_type}, Messaggio={error_msg}", file=sys.stderr)
        return f"<h1>Errore per Debug</h1><p>Per favore, invia questo messaggio all'assistente.</p><p><b>Tipo di Errore:</b> {error_type}</p><p><b>Messaggio:</b> {error_msg}</p>", 500

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible on the local network
    app.run(host='0.0.0.0', port=5001, debug=True)
