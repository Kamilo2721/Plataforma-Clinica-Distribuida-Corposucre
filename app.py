from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Estado global de los nodos
ESTADO_NODOS = {"sincelejo": True, "medellin": True, "monteria": True}

# Configuración de bases de datos con tus credenciales reales
DB_CONFIGS = {
    "sincelejo": {"host": "127.0.0.1", "port": 5431, "user": "fhir_user", "password": "fhir_password", "database": "fhir_sincelejo"},
    "medellin": {"host": "127.0.0.1", "port": 5432, "user": "fhir_user", "password": "fhir_password", "database": "fhir_medellin"},
    "monteria": {"host": "127.0.0.1", "port": 5433, "user": "fhir_user", "password": "fhir_password", "database": "fhir_bogota"}
}

def inicializar_db():
    for nodo, config in DB_CONFIGS.items():
        try:
            conn = psycopg2.connect(**config)
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS historias_clinicas (
                    id SERIAL PRIMARY KEY,
                    patient_id VARCHAR(100),
                    nombre_paciente VARCHAR(200),
                    triage_level VARCHAR(100),
                    medico_id VARCHAR(100),
                    diagnostico TEXT,
                    nodo_original VARCHAR(50),
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            conn.commit()
            cur.close()
            conn.close()
            logger.info(f"[*] Tabla verificada con éxito en el nodo: {nodo}")
        except Exception as e:
            logger.error(f"[!] Error inicializando nodo {nodo}: {e}")

@app.route('/api/clinica/registro', methods=['POST'])
def registrar():
    datos = request.json
    nodo_solicitado = datos.get("nodo")
    
    # Tolerancia a fallos (Failover)
    nodo_real = nodo_solicitado if ESTADO_NODOS.get(nodo_solicitado) else next((n for n, act in ESTADO_NODOS.items() if act), None)
    
    if not nodo_real:
        return jsonify({"error": "No hay nodos disponibles en la red"}), 503
    
    try:
        conn = psycopg2.connect(**DB_CONFIGS[nodo_real])
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO historias_clinicas (patient_id, nombre_paciente, triage_level, medico_id, diagnostico, nodo_original)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (datos['patient_id'], datos['nombre'], datos['triage'], datos['medico'], datos['diagnostico'], nodo_solicitado))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"[-] Registro guardado exitosamente en: {nodo_real}")
        return jsonify({"mensaje": f"Guardado exitosamente en la sede {nodo_real.upper()}", "nodo_real": nodo_real}), 201
    except Exception as e:
        logger.error(f"[!] Error al insertar en {nodo_real}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/clinica/reporte/<nodo>', methods=['GET'])
def obtener_reporte(nodo):
    try:
        conn = psycopg2.connect(**DB_CONFIGS[nodo])
        cur = conn.cursor()
        cur.execute("SELECT patient_id, nombre_paciente, triage_level, medico_id, diagnostico FROM historias_clinicas ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # Mapeo exacto para el Frontend Premium
        data = [
            {
                "patient_id": r[0],
                "nombre": r[1],
                "triage": r[2],
                "medico": r[3],
                "diagnostico": r[4]
            } for r in rows
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify([]), 200

@app.route('/api/nodos/estado', methods=['GET', 'POST'])
def gestionar_nodos():
    if request.method == 'POST':
        nodo = request.json.get('nodo')
        if nodo in ESTADO_NODOS:
            ESTADO_NODOS[nodo] = not ESTADO_NODOS[nodo]
    return jsonify(ESTADO_NODOS), 200

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
