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
#  Largeurs réelles (mètres)
# ===============================
OBJECT_WIDTHS = {
    "person": 0.50,
    "bottle": 0.07,
    "chair": 0.45,
    "cup": 0.08,
    "dog": 0.30,
    "cat": 0.25,
    "car": 1.75,
    "truck": 2.40,
    "bus": 2.80,
    "motorcycle": 0.85,
    "stop sign": 0.75,
    "traffic light": 0.32,
}

FOCAL_LENGTH = 900

def estimate_distance_meters(width_pixel, obj_name):
    if obj_name not in OBJECT_WIDTHS:
        return None
    real_width = OBJECT_WIDTHS[obj_name]
    distance = (real_width * FOCAL_LENGTH) / (width_pixel + 0.01)
    return round(distance, 2)

def estimate_direction(left, right, w):
    cx = (left + right) / 2
    if cx < w * 0.33:
        return "à gauche"
    elif cx > w * 0.66:
        return "à droite"
    else:
        return "devant"

def translate(name):
    return name.replace("_", " ").lower()

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

    last_time = 0
    COOLDOWN = 2

    print("🟢 YOLOv8 – Option B (danger + autres objets)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape
        detections = yolo_detect(model, frame, conf=0.45)

        if not detections:
            continue

        objects = []
        for d in detections:
            name = d["name"]
            l, t, r, b = d["box"]
            width_px = r - l
            conf = d["conf"]

            dist_m = estimate_distance_meters(width_px, name)
            if dist_m is None:
                continue

            direction = estimate_direction(l, r, w)
            proximity = "proche" if dist_m < 1.2 else "loin"
            fr_name = translate(name)

            objects.append({
                "name": fr_name,
                "dist": dist_m,
                "dir": direction,
                "prox": proximity,
                "box": (l, t, r, b)
            })

        if not objects:
            continue

        # 1️⃣ Trouver l’objet le plus dangereux (le plus proche)
        objects.sort(key=lambda x: x["dist"])
        danger = objects[0]

        # Phrase danger
        msg_danger = f"{danger['name']} {danger['dir']} à {danger['dist']} mètre, {danger['prox']}"

        # 2️⃣ Les autres objets
        others = objects[1:]
        msg_others = ""

        if len(others) > 0:
            short_list = ", ".join([f"{o['name']} {o['dir']}" for o in others[:3]])
            msg_others = f"Aussi : {short_list}"

        now = time.time()
        if (now - last_time) > COOLDOWN:
            speak(msg_danger)
            if msg_others:
                speak(msg_others)
            last_time = now

        # =========================
        #  Affichage visuel
        # =========================
        for obj in objects:
            l, t, r, b = obj["box"]
            color = (0, 255, 0) if obj["dist"] > 2 else (0, 165, 255) if obj["dist"] > 1 else (0, 0, 255)
            cv2.rectangle(frame, (l, t), (r, b), color, 2)
            cv2.putText(frame,
                        f"{obj['name']} {obj['dist']}m",
                        (l, t - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("YOLO Voice Assist – Option B", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
