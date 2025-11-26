import os
import cv2
import numpy as np
import tensorflow as tf
import time
from collections import deque

#On n’affiche une détection que si le modèle est sûr à plus de 50%
CONFIDENCE_THRESHOLD = 0.5

FPS_AVERAGE_FRAMES = 30
FOCAL_LENGTH = 1000  

KNOWN_WIDTHS = {
    'person': 0.50,
    'car': 1.75,
    'bicycle': 0.65,
    'motorcycle': 0.85,
    'bus': 2.60,
    'truck': 2.50,
    'train': 3.20,
    'dog': 0.25,
    'cat': 0.18,
    'horse': 0.90,
    'sheep': 0.40,
    'cow': 0.75,
    'chair': 0.45,
    'sofa': 1.90,
    'tv': 0.90,
    'bottle': 0.075,
    'cup': 0.08,
    'cell phone': 0.07,
    'laptop': 0.33,
    'book': 0.15,
    'stop sign': 0.75,
    'backpack': 0.30
}



model_path = os.path.join(os.getcwd(), "C:\\Users\\hp\\Desktop\\Projet AI\\SmartObstacleDetecto\\ssd_mobilenet_v2")

if not os.path.exists(model_path):
    print(f"Erreur : dossier du modèle introuvable : {model_path}")
    exit()

print("Chargement du modèle TensorFlow...")


# Détection GPU automatique
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPU détecté : {len(gpus)} appareil(s)")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
else:
    print("Exécution sur CPU")

detect_fn = tf.saved_model.load(model_path)
print("Modèle chargé !")


#dictionnaire COCO
category_index = {
    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
    6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
    11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
    16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow',
    22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack',
    28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
    35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat',
    40: 'baseball glove', 41: 'skateboard', 42: 'surfboard', 43: 'tennis racket',
    44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
    51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
    56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
    61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
    67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
    75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
    80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
    86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'
}

#Fonction de calcul de distance
def calculate_distance(object_width_pixels, object_name):
    """
    Calcule la distance en utilisant la formule : Distance = (Largeur_réelle × Focale) / Largeur_pixels
    """
    if object_name not in KNOWN_WIDTHS:
        return None
    
    real_width = KNOWN_WIDTHS[object_name]
    if object_width_pixels == 0:
        return None
    
    distance = (real_width * FOCAL_LENGTH) / object_width_pixels
    return distance

#webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur : caméra non détectée.")
    exit()

# Optimisation de la capture
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Webcam initialisée.")
print("Démarrage de la détection (Q pour quitter, S pour capture d'écran)...")

#  Variables FPS 
fps_queue = deque(maxlen=FPS_AVERAGE_FRAMES)
frame_count = 0
start_time = time.time()

#  Option d'enregistrement 
recording = False
video_writer = None

try:
    while True:
        loop_start = time.time()
        ret, frame = cap.read()
        
        if not ret:
            print("Erreur de lecture vidéo.")
            break

        frame_count += 1
        
        # Prétraitement optimisé
        input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.uint8)
        
        # Inférence
        detections = detect_fn(input_tensor)

        # Extraction résultats
        boxes = detections['detection_boxes'][0].numpy()
        classes = detections['detection_classes'][0].numpy().astype(np.int32)
        scores = detections['detection_scores'][0].numpy()

        h, w, _ = frame.shape
        detected_objects = 0

        # Affichage boîtes et calcul distances
        for i in range(len(scores)):
            if scores[i] > CONFIDENCE_THRESHOLD:
                detected_objects += 1
                ymin, xmin, ymax, xmax = boxes[i]
                left, top, right, bottom = int(xmin*w), int(ymin*h), int(xmax*w), int(ymax*h)
                
                class_name = category_index.get(classes[i], "Unknown")
                confidence = int(scores[i] * 100)
                
                # Calcul de la largeur en pixels
                object_width_pixels = right - left
                
                # Calcul de la distance
                distance = calculate_distance(object_width_pixels, class_name)
                
                # Couleur selon la distance
                if distance and distance < 1.0:
                    color = (0, 0, 255)  # Rouge (proche)
                elif distance and distance < 3.0:
                    color = (0, 165, 255)  # Orange
                else:
                    color = (0, 255, 0)  # Vert (loin)
                
                # Dessin de la boîte
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Label avec distance
                if distance:
                    label = f"{class_name} {confidence}% - {distance:.2f}m"
                else:
                    label = f"{class_name} {confidence}%"
                
                # Fond pour le texte
                (text_width, text_height), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (left, top - text_height - 10),
                            (left + text_width, top), color, -1)
                cv2.putText(frame, label, (left, top - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Calcul FPS
        loop_time = time.time() - loop_start
        fps_queue.append(1.0 / loop_time if loop_time > 0 else 0)
        current_fps = np.mean(fps_queue)

        # Affichage informations
        info_y = 30
        cv2.rectangle(frame, (5, 5), (300, 110), (0, 0, 0), -1)
        cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Objets detectes: {detected_objects}", (10, info_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, info_y + 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        status = "REC" if recording else "Q:Quitter S:Screenshot R:Record"
        cv2.putText(frame, status, (10, info_y + 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if recording else (200, 200, 200), 1)

        # Enregistrement si actif
        if recording and video_writer:
            video_writer.write(frame)

        # Affichage
        cv2.imshow("Object Detection Pro", frame)

        # Gestion clavier
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_name = f"screenshot_{int(time.time())}.jpg"
            cv2.imwrite(screenshot_name, frame)
            print(f"Capture sauvegardée : {screenshot_name}")
        elif key == ord('r'):
            if not recording:
                video_name = f"recording_{int(time.time())}.avi"
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_writer = cv2.VideoWriter(video_name, fourcc, 20.0, (w, h))
                recording = True
                print(f"Enregistrement démarré : {video_name}")
            else:
                recording = False
                if video_writer:
                    video_writer.release()
                    video_writer = None
                print("Enregistrement arrêté")

except KeyboardInterrupt:
    print("\nInterruption utilisateur")
finally:
    # Nettoyage
    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()
    
    elapsed_time = time.time() - start_time
    avg_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
    print(f"\nStatistiques :")
    print(f"   Frames traitées : {frame_count}")
    print(f"   Temps total : {elapsed_time:.2f}s")
    print(f"   FPS moyen : {avg_fps:.2f}")
    print("Programme terminé.")