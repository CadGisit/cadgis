# Main application file
import psycopg2
import psycopg2.extras
import traceback
import sys
from flask import Flask, render_template, jsonify

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

@app.route('/')
def index():
    """Mostra la tabella principale dei ponti."""
    conn = None
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
        return render_template('index.html', ponti=ponti)
    except psycopg2.Error as db_err:
        print(f"ERRORE DATABASE in index: {db_err}", file=sys.stderr)
        traceback.print_exc()
        return f"<h1>Errore di Database</h1><p>Impossibile recuperare l'elenco dei ponti. Dettagli: {db_err}</p>", 500
    except Exception as e:
        print(f"ERRORE GENERICO in index: {e}", file=sys.stderr)
        traceback.print_exc()
        return f"<h1>Errore Inaspettato</h1><p>Si è verificato un errore generico. Dettagli: {e}</p>", 500
    finally:
        if conn:
            conn.close()

@app.route('/ponte/<int:n_ponte>')
def dettaglio_ponte(n_ponte):
    """Mostra i dettagli di un singolo ponte in una maschera con tab."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Cast di campi potenzialmente problematici a TEXT per evitare errori di conversione
        query = """
            SELECT
                n_ponte, codice_iop, nome_ponte, comune, codice_istat, altri_comuni_confinanti,
                localita, tipo_sp, n_sp, nome_sp,
                CAST(progressiva_centro_km_m AS TEXT) as progressiva_centro_km_m,
                CAST(progressiva_inizio_km_m AS TEXT) as progressiva_inizio_km_m,
                CAST(progressiva_fine_km_m AS TEXT) as progressiva_fine_km_m,
                CAST(coord_x_epsg4326_centro AS TEXT) as coord_x_epsg4326_centro,
                CAST(coord_y_epsg4326_centro AS TEXT) as coord_y_epsg4326_centro,
                CAST(quota_centro AS TEXT) as quota_centro,
                classificazione, tipo_collegamento, tipo_attraversamento, n_carreggiate, n_corsie,
                luce_estesa_inferiore_6_metri,
                CAST(luce_estesa AS TEXT) as luce_estesa,
                CAST(luce_campata_max AS TEXT) as luce_campata_max,
                CAST(lungh_totale AS TEXT) as lungh_totale,
                CAST(largh_carreggiata AS TEXT) as largh_carreggiata,
                CAST(largh_fuori_tutto AS TEXT) as largh_fuori_tutto,
                n_campate, tracciato_ponte, tipologia_strutturale,
                tipologia_strutturale_voce_altro, tipologia_spalla_iniziale,
                tipologia_spalla_finale, pile_materiale_costruttivo,
                pile_materiale_costruttivo_voce_altro,
                CAST(pile_altezza_m AS TEXT) as pile_altezza_m,
                pile_geometria_sezione, pile_n_fondazioni, impalcato_materiale_costruttivo,
                impalcato_materiale_costruttivo_voce_altro, impalcato_tipologia_soletta,
                impalcato_tipologia_soletta_voce_altro, classificazione_uso_stradale,
                distretto, proprietario, classificazione_sismica_2025,
                sismicita_area_ag_g_tr475, classi_conseguenza, prp_2004,
                psda_rischio_idraulico, pai_rischio_frane, n_ispezioni_effettuate,
                data_ultima_ispezione, stato_opera, fenomeni_erosivi, fenomeni_franosi,
                morfologia_sito, tipologia_giunti, n_totale_giunti,
                CAST(lungh_giunto_spalla AS TEXT) as lungh_giunto_spalla,
                CAST(lungh_giunto_pila AS TEXT) as lungh_giunto_pila,
                apparecchi_di_appoggio, interventi_strutturali_eseguiti,
                descrizione_interventi_strutturali, limitazione_di_carico, foto_path_lizmap,
                foto_path, link_google_maps, link_streetview
            FROM prv_vb_ponti_view WHERE n_ponte = %s
        """
        cur.execute(query, (n_ponte,))
        ponte = cur.fetchone()

        if ponte is None:
            return "Ponte non trovato", 404

        return render_template('dettaglio_ponte.html', ponte=ponte)
    except psycopg2.Error as db_err:
        print(f"ERRORE DATABASE in dettaglio_ponte: {db_err}", file=sys.stderr)
        traceback.print_exc()
        return f"<h1>Errore di Database</h1><p>Impossibile recuperare i dettagli del ponte. Dettagli: {db_err}</p>", 500
    except Exception as e:
        print(f"ERRORE GENERICO in dettaglio_ponte: {e}", file=sys.stderr)
        traceback.print_exc()
        return f"<h1>Errore Inaspettato</h1><p>Si è verificato un errore generico. Dettagli: {e}</p>", 500
    finally:
        if conn:
            conn.close()

# --- DEBUG ROUTES ---

@app.route('/debug/table_structure')
def debug_table_structure():
    """Mostra la struttura della tabella/vista prv_vb_ponti_view."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'  -- O il tuo schema se diverso
            AND table_name = 'prv_vb_ponti_view';
        """
        cur.execute(query)
        structure = cur.fetchall()
        return jsonify(structure)
    except psycopg2.Error as db_err:
        return jsonify(error=str(db_err)), 500
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        if conn:
            conn.close()

@app.route('/debug/ponte/<int:n_ponte>')
def debug_ponte_raw(n_ponte):
    """Mostra i dati grezzi di un singolo ponte in formato JSON."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Seleziona tutto senza cast per vedere i dati originali
        cur.execute("SELECT * FROM prv_vb_ponti_view WHERE n_ponte = %s", (n_ponte,))
        ponte = cur.fetchone()
        if ponte is None:
            return jsonify(error="Ponte non trovato"), 404
        # Converte il RealDictRow in un dict standard per jsonify
        return jsonify(dict(ponte))
    except psycopg2.Error as db_err:
        return jsonify(error=str(db_err)), 500
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible on the local network
    app.run(host='0.0.0.0', port=5001, debug=True)
