# src/yolo/yolo_webcam.py
from src.yolo.yolo_utils import load_yolo, yolo_detect
import cv2
import os
import sys
import time
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(PROJECT_ROOT)


def estimate_distance(top, bottom, frame_h):
    bbox_h = bottom - top
    return max(0.1, 1 - bbox_h / frame_h)


def main():
    print("📦 Chargement YOLOv8...")
    model = load_yolo("yolov8n.pt")
    print("✅ Modèle YOLO chargé.")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("❌ Webcam introuvable")
        return

    fps = 0
    prev = time.time()

    print("🟢 YOLOv8 - Mode webcam (Q pour quitter)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape

        detections = yolo_detect(model, frame, conf=0.35)

        for d in detections:
            name = d["name"]
            conf = d["conf"]
            l, t, r, b = d["box"]

            dist = estimate_distance(t, b, h)

            # Couleur en fonction du danger
            if dist < 0.3:
                color = (0, 0, 255)   # Rouge
            elif dist < 0.5:
                color = (0, 165, 255)  # Orange
            else:
                color = (0, 255, 0)   # Vert

            cv2.rectangle(frame, (l, t), (r, b), color, 2)
            cv2.putText(frame,
                        f"{name} {conf:.2f} Dist:{dist:.2f}",
                        (l, t - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, color, 2)

        # FPS
        now = time.time()
        fps = 0.9 * fps + 0.1 * (1 / (now - prev))
        prev = now

        cv2.putText(frame, f"FPS: {fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255), 2)

        cv2.imshow("YOLOv8 Webcam Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
