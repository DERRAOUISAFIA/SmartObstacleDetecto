

"""
Optimization Module
-------------------
Allows:
- Confidence threshold tuning
- FPS performance analysis
- Model evaluation on webcam frames
"""

import os
import cv2
import time
import numpy as np
import tensorflow as tf

from src.utils.common import load_model, COCO_OBSTACLE_CLASSES


MODEL_DIR = os.path.join(os.getcwd(), "models", "ssd_mobilenet_v2")
detect_fn = load_model(MODEL_DIR)


def test_performance(threshold=0.5, test_frames=100):
    """
    Measures average FPS for a given confidence threshold.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam non détectée.")
        return

    print(f"🔧 Test de performance — Threshold = {threshold}")

    frame_count = 0
    start = time.time()

    while frame_count < test_frames:
        ret, frame = cap.read()
        if not ret:
            break

        tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.uint8)
        detections = detect_fn(tensor)

        scores = detections["detection_scores"][0].numpy()
        # Filtering only high confidence detections
        _ = sum(s > threshold for s in scores)

        frame_count += 1

    elapsed = time.time() - start
    fps = frame_count / elapsed if elapsed > 0 else 0

    cap.release()
    print(f"🟢 FPS moyen : {fps:.2f}")
    return fps


def compare_thresholds():
    """
    Compares FPS for different thresholds.
    """
    thresholds = [0.3, 0.5, 0.7]

    print("\n📊 Comparaison des thresholds :")
    for t in thresholds:
        fps = test_performance(threshold=t, test_frames=60)
        print(f" - Threshold {t} → {fps:.2f} FPS")
    print("\nAnalyse terminée.\n")


if __name__ == "__main__":
    print("1️⃣ - Tester FPS fixes")
    print("2️⃣ - Comparer plusieurs thresholds")
    choice = input("Choix : ")

    if choice == "1":
        thr = float(input("Threshold (0.1 à 0.9) : "))
        test_performance(threshold=thr)

    elif choice == "2":
        compare_thresholds()

    else:
        print("❌ Choix invalide.")
