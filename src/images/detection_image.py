"""
Image Detection Module
----------------------
Used for testing and validating the object detection model.
Detects objects inside a static image and shows bounding boxes.
"""

import os
import cv2
import numpy as np
import tensorflow as tf

from src.utils.common import load_model, COCO_OBSTACLE_CLASSES


MODEL_DIR = os.path.join(os.getcwd(), "models", "ssd_mobilenet_v2")
detect_fn = load_model(MODEL_DIR)


def detect_objects_in_image(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Image introuvable : {image_path}")
        return

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("⚠️ Impossible de charger l'image.")
        return

    h, w, _ = image.shape

    # Convert to tensor
    rgb_tensor = tf.convert_to_tensor(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    )[tf.newaxis, :]

    detections = detect_fn(rgb_tensor)

    boxes = detections["detection_boxes"][0].numpy()
    classes = detections["detection_classes"][0].numpy().astype(int)
    scores = detections["detection_scores"][0].numpy()

    # Visualization
    for i, score in enumerate(scores):
        if score < 0.50:
            continue

        class_id = classes[i]
        class_name = COCO_OBSTACLE_CLASSES.get(class_id, "Objet")

        ymin, xmin, ymax, xmax = boxes[i]
        left, top = int(xmin * w), int(ymin * h)
        right, bottom = int(xmax * w), int(ymax * h)

        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

        label = f"{class_name} {int(score*100)}%"
        cv2.putText(image, label, (left, top - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Image Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    img = input("Chemin de l'image à analyser : ")
    detect_objects_in_image(img)
