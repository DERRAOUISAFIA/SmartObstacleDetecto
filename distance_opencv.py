# distance.py
import cv2
import numpy as np
import math
class DistanceEstimator:
    """
    Estimation de distance approximative via la taille de l'objet en pixels.
    Chaque objet a une hauteur approximative réelle définie dans object_heights.
    """
    # Dictionnaire des hauteurs réelles par classe (en mètres)
    object_heights = {
    "person": 1.7,
    "bicycle": 1.0,
    "car": 1.5,
    "motorcycle": 1.2,
    "airplane": 3.5,
    "bus": 3.0,
    "train": 3.0,
    "truck": 3.0,
    "boat": 1.5,
    "traffic light": 2.5,
    "fire hydrant": 0.8,
    "stop sign": 2.0,
    "parking meter": 1.2,
    "bench": 0.8,
    "bird": 0.25,
    "cat": 0.25,
    "dog": 0.5,
    "horse": 1.6,
    "sheep": 0.9,
    "cow": 1.5,
    "elephant": 3.0,
    "bear": 2.0,
    "zebra": 1.5,
    "giraffe": 5.0,
    "backpack": 0.4,
    "umbrella": 1.0,
    "handbag": 0.3,
    "tie": 0.7,
    "suitcase": 0.5,
    "frisbee": 0.1,
    "skis": 1.7,
    "snowboard": 1.5,
    "sports ball": 0.3,
    "kite": 1.0,
    "baseball bat": 1.0,
    "baseball glove": 0.25,
    "skateboard": 0.3,
    "surfboard": 1.8,
    "tennis racket": 0.7,
    "bottle": 0.25,
    "wine glass": 0.2,
    "cup": 0.1,
    "fork": 0.2,
    "knife": 0.25,
    "spoon": 0.2,
    "bowl": 0.15,
    "banana": 0.2,
    "apple": 0.1,
    "sandwich": 0.1,
    "orange": 0.1,
    "broccoli": 0.15,
    "carrot": 0.2,
    "hot dog": 0.15,
    "pizza": 0.3,
    "donut": 0.1,
    "cake": 0.25,
    "chair": 0.9,
    "sofa": 1.0,
    "potted plant": 0.5,
    "bed": 1.2,
    "dining table": 0.8,
    "toilet": 0.8,
    "tvmonitor": 0.8,
    "laptop": 0.03,
    "mouse": 0.05,
    "remote": 0.2,
    "keyboard": 0.05,
    "cell phone": 0.15,
    "microwave": 0.5,
    "oven": 0.8,
    "toaster": 0.25,
    "sink": 0.8,
    "refrigerator": 1.8,
    "book": 0.3,
    "clock": 0.3,
    "vase": 0.4,
    "scissors": 0.2,
    "teddy bear": 0.5,
    "hair drier": 0.25,
    "toothbrush": 0.2,
    "hair brush": 0.25
}


    def __init__(self, known_height=1.7, focal_length_px=100):
        self.known_height = known_height
        self.focal_length_px = focal_length_px  

    def estimate_distance(self, bbox, class_name="person"):
        """
        bbox : [x1, y1, x2, y2]
        class_name : nom de la classe YOLO
        retourne distance approximative en mètres
        """
        x1, y1, x2, y2 = [int(v) for v in bbox]
        pixel_height = y2 - y1
        if pixel_height <= 0:
            return None
        
        # Utilise la hauteur réelle de l'objet si connue
        obj_height = self.object_heights.get(class_name, self.known_height)
        return (obj_height * self.focal_length_px) / pixel_height

    def classify_distance(self, dist):
        """Classifie la distance """
        if dist is None:
            return "Inconnue"
        if dist <= 1.0:
            return " Tres Proche"
        elif 1.5 <= dist <= 5.0:
            return "Proche"
        elif dist >= 5:
            return "Loin"
        else:
            return "Inconnue"

    def annotate_frame(self, frame, bboxes, distances, class_names):
        """Dessine les bboxes et distances sur le frame avec classification"""
        for bbox, dist, cls_name in zip(bboxes, distances, class_names):
            x1, y1, x2, y2 = [int(v) for v in bbox]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            dist_label = self.classify_distance(dist)
            text = f"{cls_name} - {dist_label}"
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame
