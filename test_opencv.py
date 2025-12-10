import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import time
import threading
import math
from collections import defaultdict

import cv2
from ultralytics import YOLO
from distance_opencv import DistanceEstimator
from voice_feedback import VoiceFeedback

# === INITIALISATION DU SYSTÈME ===
print("="*50)
print("SYSTEME DE DETECTION D'OBJETS AVEC FEEDBACK VOCAL")
print("="*50)

# --- LECTURE DE LA SOURCE CAMERA AVEC sys.argv ---
# server.py lance :  python test_opencv.py pc   OU   python test_opencv.py phone

if len(sys.argv) > 1:
    cam_mode = sys.argv[1].lower()
else:
    cam_mode = "pc"   # valeur par défaut

print(f"📸 Source caméra reçue depuis serveur : {cam_mode}")

use_phone_cam = cam_mode == "phone"

# --- YOLO ---
print("[1/4] Chargement du modèle YOLO...")
model = YOLO("yolo11n.pt")
print("✓ Modèle YOLO chargé")

# --- Feedback vocal ---
print("[2/4] Initialisation du feedback vocal...")
voice = VoiceFeedback(cooldown=5.0, frame_width=640, frame_height=480)
print("✓ Feedback vocal prêt")

# --- Estimateur de distance ---
print("[3/4] Initialisation de l'estimateur de distance...")
dist_estimator = DistanceEstimator()
print("✓ Estimateur prêt")

# --- Caméra ---
print("[4/4] Ouverture de la caméra...")

cap = None

if use_phone_cam:
    # URL envoyée par ton interface dans le futur (si tu veux)
    # pour l’instant on met une valeur par défaut, modifiable :
    phone_ip = "http://192.168.1.10:8080/video"
    print(f"Connexion à la caméra téléphone via {phone_ip}")
    cap = cv2.VideoCapture(phone_ip)
    if cap.isOpened():
        print(f"✓ Flux caméra téléphone ouvert : {phone_ip}")
    else:
        print("✗ Impossible d’ouvrir le flux du téléphone")
        exit()

else:
    camera_indices = [0, 1, 2]
    for idx in camera_indices:
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            print(f"✓ Caméra {idx} ouverte")
            break
    if cap is None or not cap.isOpened():
        print("✗ Aucune caméra disponible")
        exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# --- VARIABLES ---
frame_count = 0
objects_detected_total = 0
last_summary_time = time.time()
summary_interval = 15
last_announcement_time = 0
announcement_interval = 3
start_time = time.time()

print("\nCONTROLES: Q: Quitter  C: Effacer console")
print("="*50)
print("Démarrage de la détection...\n")

# === BOUCLE PRINCIPALE ===
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lecture frame")
            break

        frame_count += 1
        frame_h, frame_w = frame.shape[:2]
        if frame_w != voice.frame_width or frame_h != voice.frame_height:
            voice.update_frame_size(frame_w, frame_h)

        # Détection YOLO
        results = model(frame, imgsz=320, conf=0.4, verbose=False)
        object_counts = {}
        detected_objects = []
        current_time = time.time()

        for r in results:
            if r.boxes is not None and len(r.boxes) > 0:
                boxes = r.boxes.xyxy.cpu().numpy()
                class_ids = r.boxes.cls.cpu().numpy()
                confidences = r.boxes.conf.cpu().numpy()
                for bbox, cls_id, conf in zip(boxes, class_ids, confidences):
                    cls_name = model.names[int(cls_id)]
                    object_counts[cls_name] = object_counts.get(cls_name, 0) + 1
                    objects_detected_total += 1
                    dist = dist_estimator.estimate_distance(bbox)
                    dist_label = dist_estimator.classify_distance(dist)
                    detected_objects.append({
                        'class': cls_name,
                        'bbox': bbox,
                        'distance': dist,
                        'distance_label': dist_label,
                        'confidence': conf
                    })

        # Annonce des objets les plus proches
        if detected_objects and (current_time - last_announcement_time >= announcement_interval):
            detected_objects.sort(key=lambda x: x['confidence'], reverse=True)
            obj = detected_objects[0]
            voice.announce_object(
                class_name=obj['class'],
                distance_label=obj['distance_label'],
                bbox=obj['bbox']
            )
            last_announcement_time = current_time

        # Annotation frame
        if detected_objects:
            bboxes = [obj['bbox'] for obj in detected_objects]
            distances = [obj['distance'] for obj in detected_objects]
            class_names = [obj['class'] for obj in detected_objects]
            frame = dist_estimator.annotate_frame(frame, bboxes, distances, class_names)

        # Infos à l’écran
        info_text = [
            f"Frame: {frame_count}",
            f"Objets: {len(detected_objects)}",
            f"Total: {objects_detected_total}"
        ]
        for i, text in enumerate(info_text):
            y = 30 + i*25
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
        cv2.putText(frame, "Q: quitter  C: effacer console", (10, frame_h-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("Détection objets - Feedback vocal", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): 
            break
        elif key == ord('c'):
            print("\n"*50)

except KeyboardInterrupt:
    print("Interruption par l'utilisateur")
finally:
    cap.release()
    cv2.destroyAllWindows()
    voice.cleanup()

    print("\nSTATISTIQUES:")
    print(f"  Frames traités: {frame_count}")
    print(f"  Objets détectés: {objects_detected_total}")
    print(f"  FPS moyen: {frame_count/max(1, time.time()-start_time):.1f}")
    print("PROGRAMME TERMINÉ")
