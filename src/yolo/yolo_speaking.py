# src/yolo/yolo_speaking.py
from src.yolo.yolo_utils import load_yolo, yolo_detect
import pyttsx3
import cv2
import os
import sys
import time
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(PROJECT_ROOT)


# ===============================
#  Synthèse vocale
# ===============================
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()


# ===============================
#  Distance + direction
# ===============================
def estimate_distance(top, bottom, h):
    bbox_h = bottom - top
    return max(0.1, 1 - bbox_h / h)


def estimate_direction(left, right, w):
    cx = (left + right) / 2
    if cx < w * 0.33:
        return "à gauche"
    elif cx > w * 0.66:
        return "à droite"
    else:
        return "devant"


# ===============================
#  Classes utiles pour malvoyants
# ===============================
USEFUL_CLASSES = [
    "person", "car", "truck", "bus", "motorcycle",
    "stop sign", "traffic light",
    "dog", "cat",
]


# Traduction FR
TRANSLATE = {
    "person": "personne",
    "car": "voiture",
    "truck": "camion",
    "bus": "bus",
    "motorcycle": "moto",
    "stop sign": "panneau stop",
    "traffic light": "feu tricolore",
    "dog": "chien",
    "cat": "chat",
}


# ===============================
#  Boucle principale
# ===============================
def main():
    print("📦 Chargement YOLOv8...")
    model = load_yolo("yolov8n.pt")
    print("✅ Modèle chargé.")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    last_message = ""
    last_time = 0
    last_distance = None
    missing_frames = 0

    COOLDOWN = 1.5
    DANGER_REPEAT = 2.5
    APPROACH_THRESHOLD = 0.12  # 12 % différence de distance

    print("🟢 YOLOv8 – Mode vocal PRO (Q pour quitter)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape
        detections = yolo_detect(model, frame, conf=0.35)

        # Filtrer seulement les objets utiles
        usable = [d for d in detections if d["name"] in USEFUL_CLASSES]

        if not usable:
            missing_frames += 1
            if missing_frames > 8:
                last_message = ""
            continue
        else:
            missing_frames = 0

        # Prendre l’objet le plus proche / dangereux
        best = None
        best_score = -1

        for d in usable:
            name = d["name"]
            l, t, r, b = d["box"]
            dist = estimate_distance(t, b, h)
            conf = d["conf"]

            score = (1.3 - dist) + conf
            if score > best_score:
                best_score = score
                best = (name, l, t, r, b, dist)

        if best is None:
            continue

        name, l, t, r, b, dist = best
        direction = estimate_direction(l, r, w)

        name_fr = TRANSLATE.get(name, name)
        dist_text = "proche" if dist < 0.4 else "loin"
        message = f"{name_fr} {direction}, {dist_text}"

        now = time.time()

        # Première annonce ou réapparition
        if last_message == "":
            speak(message)
            last_message, last_time, last_distance = message, now, dist

        # Rapprochement / éloignement
        elif last_distance is not None and abs(dist - last_distance) > APPROACH_THRESHOLD:
            if dist < last_distance:
                speak("Il se rapproche")
            else:
                speak("Il s'éloigne")
            speak(message)
            last_message, last_time, last_distance = message, now, dist

        # Danger répété
        elif dist < 0.4 and (now - last_time) > DANGER_REPEAT:
            speak(message)
            last_message, last_time, last_distance = message, now, dist

        # Cooldown normal
        elif (now - last_time) > COOLDOWN:
            speak(message)
            last_message, last_time, last_distance = message, now, dist

        else:
            last_distance = dist

        # Affichage
        color = (0, 255, 0) if dist > 0.5 else (
            0, 165, 255) if dist > 0.3 else (0, 0, 255)
        cv2.rectangle(frame, (l, t), (r, b), color, 2)
        cv2.putText(frame, message, (l, t - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("YOLO Voice Assist", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
