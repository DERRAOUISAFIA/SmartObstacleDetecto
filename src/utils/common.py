"""
Common utilities for SmartObstacleDetector
------------------------------------------
Central functions shared across all modules:
- model loading
- COCO categories (extended for useful obstacles)
- direction estimation
- distance estimation
"""

import os
import tensorflow as tf


# ==============================
#  Load TensorFlow model
# ==============================

def load_model(model_dir):
    """Loads a TensorFlow SavedModel from the given directory."""
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"❌ Model folder not found : {model_dir}")

    print("📦 Loading TensorFlow model...")
    model = tf.saved_model.load(model_dir)
    print("✅ Model loaded.")
    return model


# ==============================
#  Direction estimation
# ==============================

def get_direction(left, right, frame_width):
    """Returns 'à gauche', 'à droite', or 'devant' based on bbox position."""
    center_x = (left + right) / 2

    if center_x < frame_width * 0.33:
        return "à gauche"
    elif center_x > frame_width * 0.66:
        return "à droite"
    else:
        return "devant"


# ==============================
#  Distance estimation
# ==============================

def estimate_distance_from_bbox(top, bottom, frame_height):
    """
    Approximate distance based on bounding box height.
    Larger bbox = object closer.
    Returns a value between 0.2 and 1.0.
    """
    bbox_height = bottom - top
    return max(0.2, 1 - bbox_height / frame_height)


# ==============================
#  COCO classes (extended)
# ==============================
# This set includes ONLY objects useful for visually impaired users.

COCO_OBSTACLE_CLASSES = {
    # Humains
    1: "personne",

    # Véhicules
    2: "vélo",
    3: "voiture",
    4: "moto",
    6: "bus",
    8: "camion",

    # Panneaux et signalisations
    10: "feu tricolore",
    11: "borne incendie",
    13: "panneau stop",

    # Animaux
    17: "chat",
    18: "chien",

    # Objets pertinents
    44: "bouteille",
    47: "tasse",
    62: "chaise",
    63: "canapé",
    73: "ordinateur",
    77: "téléphone",
}
