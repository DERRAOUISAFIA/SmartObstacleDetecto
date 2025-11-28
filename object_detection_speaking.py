import os
import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
import time
import threading

# ======================
#  Chargement du modèle
# ======================
model_path = os.path.join(os.getcwd(), "ssd_mobilenet_v2")
detect_fn = tf.saved_model.load(model_path)
print("📦 Model loaded!")

# ======================
#  Classes COCO
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
#  Synthèse vocale async
# ======================
def speak_async(text):
    threading.Thread(target=lambda: engine_say(text), daemon=True).start()

def engine_say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

# ======================
#  Construction phrase naturelle
# ======================
def build_sentence(objects):
    if len(objects) == 0:
        return None

    objects = sorted(objects)  # ordre propre
    if len(objects) == 1:
        return f"Object detected ahead: {objects[0]}."
    else:
        # A, B and C
        return "Objects detected ahead: " + ", ".join(objects[:-1]) + f" and {objects[-1]}."

# Anti-spam
last_spoken = ""
last_time = 0
speak_interval = 2.0

# ======================
#  Caméra
# ======================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not detected.")
    exit()

print("🎥 Webcam ready. Press Q to quit.")

# ======================
#  Boucle principale
# ======================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # TensorFlow input
    input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.uint8)
    detections = detect_fn(input_tensor)

    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int32)
    scores = detections['detection_scores'][0].numpy()

    h, w, _ = frame.shape

    current_objects = []

    # --- Collecter TOUS les objets
    for i in range(len(scores)):
        if scores[i] > 0.5:
            class_name = category_index.get(classes[i], "Unknown")
            current_objects.append(class_name)

            ymin, xmin, ymax, xmax = boxes[i]
            left, top, right, bottom = int(xmin*w), int(ymin*h), int(xmax*w), int(ymax*h)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Liste unique
    unique_objects = list(set(current_objects))

    # Construire phrase
    sentence = build_sentence(unique_objects)

    # Parler sans spam
    now = time.time()
    if sentence and (sentence != last_spoken or now - last_time > speak_interval):
        speak_async(sentence)
        last_spoken = sentence
        last_time = now

    cv2.imshow("Object Detection with Voice", cv2.resize(frame, (900, 700)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("👋 Program closed.")
