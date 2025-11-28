# src/yolo/yolo_image.py
from src.yolo.yolo_utils import load_yolo, yolo_detect
import cv2
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(PROJECT_ROOT)


def main():
    model = load_yolo("yolov8n.pt")

    img_path = input("Chemin de l'image : ").strip()

    if not os.path.exists(img_path):
        print("❌ Image introuvable")
        return

    img = cv2.imread(img_path)
    detections = yolo_detect(model, img, conf=0.35)

    for d in detections:
        l, t, r, b = d["box"]
        name = d["name"]
        conf = d["conf"]

        cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(
            img,
            f"{name} {conf:.2f}",
            (l, t - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("YOLOv8 - Image Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
