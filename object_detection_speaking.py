import os
import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
import time

# ======================
#  Chargement du modèle
# ======================
model_path = os.path.join(os.getcwd(), "ssd_mobilenet_v2")

if not os.path.exists(model_path):
    print(f"❌ Erreur : dossier du modèle introuvable : {model_path}")
    print("➡️ Vérifiez que le modèle a bien été téléchargé et extrait.")
    exit()

print("📦 Chargement du modèle TensorFlow...")
detect_fn = tf.saved_model.load(model_path)
print("✅ Modèle chargé avec succès !")

# ======================
#  Classes COCO utiles
# ======================
category_index = {
    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
    6: 'bus', 7: 'train', 8: 'truck', 9: 'boat',
    10: 'traffic light', 13: 'stop sign',
    17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow',
    44: 'bottle', 47: 'cup', 48: 'fork', 49: 'knife',
    50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple',
    55: 'orange', 56: 'broccoli', 57: 'carrot',
    73: 'book', 75: 'remote', 77: 'cell phone',
    78: 'microwave', 84: 'clock',
    86: 'vase', 87: 'scissors', 88: 'teddy bear',
    89: 'hair drier', 90: 'toothbrush'
}

# ======================
#  Synthèse vocale
# ======================
engine = pyttsx3.init()
engine.setProperty('rate', 160)   # vitesse de parole

# ======================
#  Caméra
# ======================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Erreur : caméra non détectée.")
    exit()

print("🎥 Webcam détectée.")
print("🟢 Démarrage de la détection (appuyez sur Q pour quitter)...")

# ======================
#  Anti-répétition audio
# ======================
last_spoken = ""
last_time = 0
speak_interval = 2.0  # secondes minimum entre annonces

# ======================
#       Boucle
# ======================
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Erreur de lecture vidéo.")
        break

    # Convertir image pour TF
    input_tensor = tf.convert_to_tensor(
        np.expand_dims(frame, 0), dtype=tf.uint8)
    detections = detect_fn(input_tensor)

    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int32)
    scores = detections['detection_scores'][0].numpy()

    h, w, _ = frame.shape
    current_objects = []

    # Parcourir détections
    for i in range(len(scores)):
        if scores[i] > 0.5:
            ymin, xmin, ymax, xmax = boxes[i]
            left, top, right, bottom = int(
                xmin*w), int(ymin*h), int(xmax*w), int(ymax*h)
            class_name = category_index.get(classes[i], "Unknown")
            current_objects.append(class_name)

            # Dessin boîtes
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} ({int(scores[i]*100)}%)",
                        (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)

    # Synthèse vocale stabilisée
    now = time.time()
    for obj in set(current_objects):
        if obj != last_spoken or now - last_time > speak_interval:
            engine.say(f"{obj} ahead")
            last_spoken = obj
            last_time = now

    engine.runAndWait()

    # Affichage vidéo
    cv2.imshow('Object Detection with Voice', cv2.resize(frame, (900, 700)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("👋 Fermeture du programme.")
