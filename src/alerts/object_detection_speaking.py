"""
SmartObstacleDetector — Assistant Vocal Intelligent
---------------------------------------------------
Version MAx améliorée :
- Détecte TOUS les obstacles utiles pour malvoyants
- Priorité intelligente (personne > voiture > animaux > panneau)
- Détection stable (filtrage sur plusieurs frames)
- Réapparition fiable pour n'importe quel obstacle
- Alertes vocales cohérentes et naturelles
- Détection d'approche / éloignement
- Répétition danger
- Cooldown intelligent
"""

import os
import cv2
import time
import numpy as np
import tensorflow as tf
import pyttsx3


# =============== Synthèse vocale ==================

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()


# =============== Charger modèle ====================

MODEL_DIR = os.path.join(os.getcwd(), "models", "ssd_mobilenet_v2")
print("📦 Chargement du modèle...")
detect_fn = tf.saved_model.load(MODEL_DIR)
print("✅ Modèle chargé.")


# =============== Obstacles utiles ===================

# Classes prioritaires pour malvoyants
OBSTACLES = {
    1: "personne",
    3: "voiture",
    4: "moto",
    6: "bus",
    8: "camion",
    10: "feu tricolore",
    13: "panneau stop",
    17: "chat",
    18: "chien",
}

# Priorité (pour choisir quoi annoncer dans un environnement chargé)
PRIORITY = {
    "personne": 5,
    "voiture": 4,
    "camion": 4,
    "bus": 4,
    "moto": 3,
    "chien": 3,
    "chat": 2,
    "panneau stop": 1,
    "feu tricolore": 1,
}


# =============== Calcul direction & distance ==================

def estimate_distance(top, bottom, h):
    bbox_h = bottom - top
    return max(0.12, 1 - bbox_h / h)


def estimate_direction(left, right, w):
    c = (left + right) / 2
    if c < w * 0.33:
        return "à gauche"
    elif c > w * 0.66:
        return "à droite"
    return "devant"


# =============== Variables globales ==================

last_message = ""
last_distance = None
last_time = 0
missing_frames = 0

COOLDOWN = 1.6
DANGER_REPEAT = 2.3
APPROACH_THRESHOLD = 0.10


# =============== Boucle principale ==================

def run_smart_voice_detector():

    global last_message, last_distance, last_time, missing_frames

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("❌ Webcam non détectée.")
        return

    print("🟢 Assistant Vocal — Q pour quitter")

    stable_history = {}     # {name: [dist1, dist2, dist3]}

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape

        # Inference
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (640, 480))
        tensor = tf.convert_to_tensor(resized)[tf.newaxis, :]

        detections = detect_fn(tensor)

        boxes = detections["detection_boxes"][0].numpy()
        classes = detections["detection_classes"][0].numpy().astype(int)
        scores = detections["detection_scores"][0].numpy()

        candidates = []

        # Détection de TOUS les obstacles utiles
        for i, sc in enumerate(scores):
            if sc < 0.50:
                continue

            cid = classes[i]
            if cid not in OBSTACLES:
                continue

            ymin, xmin, ymax, xmax = boxes[i]
            left, top = int(xmin*w), int(ymin*h)
            right, bottom = int(xmax*w), int(ymax*h)

            name = OBSTACLES[cid]
            dist = estimate_distance(top, bottom, h)
            direc = estimate_direction(left, right, w)

            prio = PRIORITY[name] * (1.4 - dist)

            candidates.append((name, direc, dist, prio))

            # Dessin
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        now = time.time()

        # Aucun obstacle
        if len(candidates) == 0:
            missing_frames += 1
            if missing_frames > 10:
                last_message = ""
                last_distance = None
                last_time = 0
            cv2.imshow("SmartObstacleDetector", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        missing_frames = 0

        # Choisir l’obstacle le plus important
        best = max(candidates, key=lambda x: x[3])  # par priorité
        name, direc, dist, _ = best

        message = f"{name} {direc}, {'proche' if dist < 0.40 else 'loin'}"

        # Filtrage de stabilité
        if name not in stable_history:
            stable_history[name] = []
        stable_history[name].append(dist)
        if len(stable_history[name]) < 3:
            continue
        if len(stable_history[name]) > 3:
            stable_history[name].pop(0)

        # Réapparition
        if last_message == "":
            speak(message)
            last_message = message
            last_distance = dist
            last_time = now

        # Approche / éloignement
        elif abs(dist - last_distance) > APPROACH_THRESHOLD:
            if dist < last_distance:
                speak("Attention, il se rapproche")
            else:
                speak("Il s'éloigne")
            speak(message)
            last_message = message
            last_distance = dist
            last_time = now

        # Danger
        elif dist < 0.40 and (now - last_time) > DANGER_REPEAT:
            speak("Attention, danger proche")
            speak(message)
            last_message = message
            last_distance = dist
            last_time = now

        # Message normal après cooldown
        elif (now - last_time) > COOLDOWN:
            speak(message)
            last_message = message
            last_distance = dist
            last_time = now

        else:
            last_distance = dist

        cv2.imshow("SmartObstacleDetector", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_smart_voice_detector()
