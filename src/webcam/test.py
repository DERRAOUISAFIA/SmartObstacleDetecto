"""
Webcam Detection Module
-----------------------
Features:
- Real-time detection
- FPS computation
- Distance estimation using focal length
- Color-coded bounding boxes
- Screenshot + video recording
"""

from src.utils.common import COCO_OBSTACLE_CLASSES as COCO_INDEX
import os
import cv2
import time
import numpy as np
import tensorflow as tf
from collections import deque

from src.utils.common import (
    load_model,
    get_direction,
    estimate_distance_from_bbox,
)


CONFIDENCE_THRESHOLD = 0.5
FPS_AVERAGE_FRAMES = 30
FOCAL_LENGTH = 1000


# COCO classes for display


MODEL_DIR = os.path.join(os.getcwd(), "models", "ssd_mobilenet_v2")
detect_fn = load_model(MODEL_DIR)


def calculate_distance(object_width_pixels, object_name):
    """
    Distance formula:
        distance = (real_width × focal) / pixels
    """

    KNOWN_WIDTHS = {
        'personne': 0.50,
        'voiture': 1.75,
        'moto': 0.85,
        'bus': 2.60,
        'camion': 2.50,
        'chien': 0.25,
        'chat': 0.18
    }

    if object_name not in KNOWN_WIDTHS:
        return None

    real_width = KNOWN_WIDTHS[object_name]
    distance = (real_width * FOCAL_LENGTH) / max(object_width_pixels, 1)
    return distance


def run_webcam_detector():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam non détectée.")
        return

    fps_queue = deque(maxlen=FPS_AVERAGE_FRAMES)
    recording = False
    video_writer = None
    frame_count = 0

    print("🎥 Webcam active — Q : Quitter | S : Screenshot | R : Record")

    try:
        while True:
            loop_start = time.time()

            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape

            # Model input
            tensor = tf.convert_to_tensor(
                np.expand_dims(frame, 0), dtype=tf.uint8)
            detections = detect_fn(tensor)

            boxes = detections["detection_boxes"][0].numpy()
            classes = detections["detection_classes"][0].numpy().astype(int)
            scores = detections["detection_scores"][0].numpy()

            detected_objects = 0

            # ==============================
            #  Detection loop
            # ==============================
            for i, score in enumerate(scores):
                if score < CONFIDENCE_THRESHOLD:
                    continue

                class_id = classes[i]
                class_name = COCO_INDEX.get(class_id, "Objet")

                ymin, xmin, ymax, xmax = boxes[i]
                left, top = int(xmin * w), int(ymin * h)
                right, bottom = int(xmax * w), int(ymax * h)

                detected_objects += 1
                object_width_px = right - left

                distance = calculate_distance(object_width_px, class_name)

                # Color by distance
                if distance and distance < 1:
                    color = (0, 0, 255)     # Red
                elif distance and distance < 3:
                    color = (0, 165, 255)   # Orange
                else:
                    color = (0, 255, 0)     # Green

                # Drawing
                label = f"{class_name} {int(score*100)}%"
                if distance:
                    label += f" - {distance:.2f}m"

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # ==============================
            #  FPS computation
            # ==============================
            loop_time = time.time() - loop_start
            fps_queue.append(1 / loop_time if loop_time > 0 else 0)
            fps = np.mean(fps_queue)

            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Objets : {detected_objects}", (10, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # ==============================
            #  Screenshot & Recording
            # ==============================
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            elif key == ord("s"):
                img_name = f"screenshot_{int(time.time())}.jpg"
                cv2.imwrite(img_name, frame)
                print(f"📸 Screenshot : {img_name}")

            elif key == ord("r"):
                if not recording:
                    video_name = f"video_{int(time.time())}.avi"
                    fourcc = cv2.VideoWriter_fourcc(*"XVID")
                    video_writer = cv2.VideoWriter(
                        video_name, fourcc, 20.0, (w, h))
                    recording = True
                    print(f"🔴 Enregistrement : {video_name}")
                else:
                    recording = False
                    video_writer.release()
                    video_writer = None
                    print("⏹️ Enregistrement arrêté")

            if recording and video_writer:
                video_writer.write(frame)

            cv2.imshow("SmartObstacleDetector - Webcam", frame)

    finally:
        cap.release()
        if video_writer:
            video_writer.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run_webcam_detector()
