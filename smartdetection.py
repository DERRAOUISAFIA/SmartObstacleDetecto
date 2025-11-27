import os
import cv2
import numpy as np
import tensorflow as tf
import time
import pyttsx3

# === Synthèse vocale (en français) ===
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    print("🗣️ ", text)
    engine.say(text)
    engine.runAndWait()


last_message = ""
last_time_spoken = 0
cooldown = 2.5   # éviter spam audio

# === Chargement modèle ===
model_path = os.path.join(os.getcwd(), "ssd_mobilenet_v2")

print("📦 Chargement du modèle...")
detect_fn = tf.saved_model.load(model_path)
print("✅ Modèle chargé.")

# === Classes utiles pour un aveugle (obstacles majeurs) ===
OBSTACLES = {
    1: "personne",
    3: "voiture",
    4: "moto",
    6: "bus",
    8: "camion",
    10: "feu de signalisation",
    13: "panneau stop",
    17: "chat",
    18: "chien"
}

# === Webcam ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Caméra non détectée.")
    exit()

print("🟢 Détection intelligente — Q pour quitter")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # → Format pour TensorFlow
    input_tensor = tf.convert_to_tensor(
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))[tf.newaxis, :]

    # → Détection
    detections = detect_fn(input_tensor)

    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(int)
    scores = detections['detection_scores'][0].numpy()

    detected_object = None
    best_score = 0
    obstacle_info = None

    # === Choisir l’objet le plus dangereux et le plus proche ===
    for i in range(len(scores)):
        if scores[i] < 0.60:
            continue

        class_id = classes[i]
        if class_id not in OBSTACLES:
            continue  # On ignore les objets inutiles

        ymin, xmin, ymax, xmax = boxes[i]
        left, top = int(xmin * w), int(ymin * h)
        right, bottom = int(xmax * w), int(ymax * h)

        obj_name = OBSTACLES[class_id]

        # Distance APPROX via hauteur de la bbox (plus c’est grand = plus proche)
        bbox_height = bottom - top
        distance = max(0.2, 1 - bbox_height / h)  # entre 0.2 et 1

        # Direction
        center_x = (left + right) / 2
        if center_x < w * 0.33:
            direction = "à gauche"
        elif center_x > w * 0.66:
            direction = "à droite"
        else:
            direction = "devant"

        # Garder le plus proche
        if scores[i] > best_score:
            best_score = scores[i]
            obstacle_info = (obj_name, direction, distance)

        # Dessin
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, obj_name,
                    (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)

    # === Message vocal ===
    if obstacle_info:
        name, direction, distance = obstacle_info
        dist_text = "proche" if distance < 0.45 else "loin"

        message = f"{name} {direction}, {dist_text}"

        current_time = time.time()

        if message != last_message or (current_time - last_time_spoken) > cooldown:
            speak(message)
            last_message = message
            last_time_spoken = current_time

    cv2.imshow("Smart Obstacle Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
