import os
import cv2
import time
import numpy as np
import tensorflow as tf
import pyttsx3
import threading


engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(text):
 engine.say(text)
 engine.runAndWait()

def speak_async(text):
 threading.Thread(target=speak, args=(text,), daemon=True).start()


MODEL_DIR = os.path.join(os.getcwd(), "models", "ssd_mobilenet_v2")
print("📦 Chargement du modèle...")
detect_fn = tf.saved_model.load(MODEL_DIR)
print("✅ Modèle chargé.")


OBSTACLES = {
1: "personne", 3: "voiture", 4: "moto", 6: "bus", 8: "camion",
10: "feu tricolore", 13: "panneau stop", 17: "chat", 18: "chien"
}

PRIORITY = {
"personne": 5, "voiture": 4, "camion": 4, "bus": 4, "moto": 3,
"chien": 3, "chat": 2, "panneau stop": 1, "feu tricolore": 1
}


def estimate_distance(top, bottom, h):
 bbox_h = bottom - top
 return max(0.12, 1 - bbox_h / h)

def estimate_direction(left, right, w):
 c = (left + right) / 2
 if c < w * 0.33: return "à gauche"
 elif c > w * 0.66: return "à droite"
 return "devant"

# Historique de stabilité et dernier état
stable_history = {} # {name: [dist1, dist2, dist3]}
last_state = {} # {name: (message, dist)}
APPROACH_THRESHOLD = 0.10
MIN_COOLDOWN = 0.5 # secondes entre messages similaires


def run_smart_voice_detector():
 
 
 cap = cv2.VideoCapture(0)
 cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
 cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
 if not cap.isOpened():
  print("❌ Webcam non détectée.")
  return

 print("🟢 Assistant Vocal — Q pour quitter")
 missing_frames = 0
 last_time_spoken = 0

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

    for i, sc in enumerate(scores):
        if sc < 0.5: continue
        cid = classes[i]
        if cid not in OBSTACLES: continue

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

    if len(candidates) == 0:
        missing_frames += 1
        if missing_frames > 10:
            stable_history.clear()
            last_state.clear()
        cv2.imshow("SmartObstacleDetector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    missing_frames = 0

    # Choisir le plus prioritaire
    best = max(candidates, key=lambda x: x[3])
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

    # Construire message complet
    messages = [message]
    last_msg, last_dist = last_state.get(name, ("", None))
    if last_dist is not None and abs(dist - last_dist) > APPROACH_THRESHOLD:
        if dist < last_dist:
            messages.append("Attention, il se rapproche")
        else:
            messages.append("Il s'éloigne")
    if dist < 0.40:
        messages.append("Attention, danger proche")

    full_message = ". ".join(messages)

    # Ne pas répéter le même message si identique
    if full_message != last_msg or abs(dist - last_dist) > APPROACH_THRESHOLD:
        speak_async(full_message)
        last_state[name] = (full_message, dist)
        last_time_spoken = now

    cv2.imshow("SmartObstacleDetector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

 cap.release()
 cv2.destroyAllWindows()

if __name__== "__main__":
   run_smart_voice_detector() 