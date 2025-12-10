from flask import Flask, request
from flask_cors import CORS
import subprocess
import threading

app = Flask(__name__)
CORS(app)

PYTHON_PATH = r"C:\Users\Lenovo\Desktop\Python IA\SmartObstacleDetecto\blindenv\Scripts\python.exe"

process = None
process_lock = threading.Lock()

def run_script(script_path):
    global process
    with process_lock:
        if process is None:
            print(f"🔧 Lancement du script : {script_path}")
            process = subprocess.Popen([PYTHON_PATH, script_path])
        else:
            print("⚠️ Un processus est déjà en cours !")

@app.route("/start", methods=["POST"])
def start_detection():
    data = request.get_json()
    print("🚨 Données reçues :", data)  # ← TRACE ICI

    mode = data.get("mode") if data else None

    if mode == "yolo":
        script = "src/yolo/yolo_speaking.py"
    elif mode == "speaking":
        script = "src/alerts/object_detection_speaking.py"
    else:
        print("❌ Mode invalide reçu :", mode)
        return "❌ Mode invalide", 400

    threading.Thread(target=run_script, args=(script,), daemon=True).start()
    return f"Mode {mode} lancé !", 200


@app.route("/stop")
def stop_detection():
    global process
    with process_lock:
        if process is not None:
            print("🛑 Arrêt du processus")
            process.terminate()
            process = None
            return "Détection arrêtée !", 200
        else:
            return "Aucun processus en cours", 200

if __name__ == "__main__":
    print("🚀 Serveur Flask prêt sur http://localhost:5000")
    app.run(port=5000)
