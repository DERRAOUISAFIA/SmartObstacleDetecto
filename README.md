# SmartObstacleDetector — Assistant de Détection d’Obstacles pour Personnes Malvoyantes

## 📌 1. Introduction

SmartObstacleDetector est un système d’assistance visuelle conçu pour aider les personnes malvoyantes à se déplacer en toute sécurité.  
Il détecte les obstacles en temps réel, estime leur distance et leur direction, et peut annoncer vocalement les dangers.

Le projet comprend **deux générations de prototypes** :

### 🔹 Prototype 1 — SSD MobileNet V2 (TensorFlow)
- Détection en temps réel  
- Distance + direction  
- Module vocal simple  
- Version de base pour étude comparative  

### 🔹 Prototype 2 — YOLOv8 (Version Finale)
- Détection **ultra-précise et rapide**  
- 10 à 30 FPS sur webcam  
- Alerte vocale intelligente en français  
- Stabilité améliorée  
- Meilleure gestion des distances / directions / re-détection  

Ce README documente l’architecture finale du projet.

---

## ⭐ 2. Fonctionnalités Principales

### 🟩 2.1 Détection d’Objets en Temps Réel (YOLOv8 — Version Finale)

- Détection rapide et fiable  
- Très haute précision  
- Fonctionne sur webcam, caméras USB et vidéos  
- Suivi d’objets prioritaires :  
  **personne, voiture, camion, moto, autobus, chien, chat, panneau stop, feu tricolore**

#### 🟩 Couleurs des boîtes :
- 🟥 **Rouge** : danger — objet très proche  
- 🟧 **Orange** : distance moyenne  
- 🟩 **Vert** : zone sûre  

---

### 🟦 2.2 Alerte Vocale Intelligente (Final YOLO)

Module vocal **hors-ligne**, en français, basé sur `pyttsx3`.

Fonctionnalités :
- Détection directionnelle :  
  **“à gauche”**, **“à droite”**, **“devant”**
- Estimation de distance :  
  **“proche / loin”**
- Mouvements :  
  **“Il se rapproche”**, **“Il s’éloigne”**
- Anti-spam vocal intelligent  
- Réinitialisation automatique lors de la disparition  
- Re-détection instantanée  

> 🎤 **C’est le module principal à présenter au jury**

---

### 🟧 2.3 Modules MobileNet (Prototype 1)

Toujours inclus pour comparaison académique :

- Détection webcam  
- Estimation de distance (via focale)  
- Capture écran / vidéo  
- Analyse d’image fixe  
- Module vocal basique  
- Optimisation FPS & seuils  

---

### 🟨 2.4 Module de Détection d’Images (YOLO + MobileNet)

- Analyse de photos  
- Affichage des bounding boxes  
- Tests pour valider le modèle  
- Compatible avec les deux architectures  

---

### 🟪 2.5 Module d’Optimisation

- Comparaison : YOLO vs MobileNet  
- Test des seuils de confiance  
- Analyse de performances  
- Benchmark complet  

---

## 👥 3. Répartition du Travail

| Membre | Fichier | Rôle |
|-------|---------|------|
| **Membre 1 — Détection Image** | `src/images/detection_image.py` | Détection sur image, visualisation |
| **Membre 2 — Webcam + Distance** | `src/webcam/test.py` | Détection temps réel, estimation distance, FPS |
| **Membre 3 — Module Vocal (Version Finale)** | `src/yolo/yolo_speaking.py` | Alerte vocale intelligente |
| **Membre 4 — Optimisation** | `src/optimization/optimization.py` | Analyse, tuning, comparaison modèles |

---

## 🗂️ 4. Structure du Projet



SmartObstacleDetector/
│
├── src/
│ ├── yolo/ # Version finale YOLO
│ │ ├── yolo_utils.py
│ │ ├── yolo_image.py
│ │ ├── yolo_webcam.py
│ │ └── yolo_speaking.py
│ │
│ ├── alerts/ # Ancienne version vocale
│ │ └── object_detection_speaking_old.py
│ │
│ ├── images/
│ │ └── detection_image.py
│ │
│ ├── webcam/
│ │ └── test.py
│ │
│ ├── utils/
│ │ └── common.py
│ │
│ └── optimization/
│ └── optimization.py
│
├── models/
│ └── ssd_mobilenet_v2/
│
├── assets/ # Images, captures, GIFs (optionnel)
│
├── requirements.txt
└── README.md

---

## ⚙️ 5. Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/your-repo/SmartObstacleDetector.git
cd SmartObstacleDetector
2️⃣ Créer un environnement virtuel
macOS / Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
3️⃣ Installer les dépendances
pip install -r requirements.txt
▶️ 6. Exécution du Projet
🎥 Détection Webcam (YOLO — recommandé)
python src/yolo/yolo_webcam.py
🔊 Détection + Alerte Vocale (YOLO)
python src/yolo/yolo_speaking.py
🖼 Détection d’Images (YOLO)
python src/yolo/yolo_image.py
📌 Prototype MobileNet (ancienne version)
Module vocal :
python src/alerts/object_detection_speaking_old.py
Détection image :
python src/images/detection_image.py
Détection webcam :
python src/webcam/test.py
Optimisation :
python src/optimization/optimization.py
🤖 7. Modèles Utilisés
🚀 YOLOv8 (Version Finale)
Fichier : yolov8n.pt
Très rapide (temps réel)
Compatible CPU
📦 SSD MobileNet V2 (Prototype 1)
Pré-entraîné sur COCO (90 classes)
Faible consommation de ressources
🛠️ 8. Technologies Utilisées
Technologie	Rôle
YOLOv8	Détection avancée
TensorFlow 2	Prototype MobileNet
OpenCV	Webcam / Vidéo
pyttsx3	Synthèse vocale hors-ligne
NumPy	Calcul
Python 3.10+	Langage
🎤 9. Déroulement de la Présentation (Jury)
Introduction — Membre 4
Prototype 1 : Détection d’Images — Membre 1
Prototype 1 : Webcam + Distance — Membre 2
Prototype 2 : YOLO Vocal — Membre 3
Comparaison modèles & Optimisation — Membre 4
Conclusion & perspectives
🔮 10. Améliorations Futures
✔ Application mobile
✔ Détection d’escaliers / trous
✔ Capteurs (Ultrasonic, LiDAR)
✔ Navigation GPS
✔ Retour haptique (vibrations)
✔ Version wearable (lunettes, gilet, canne intelligente)
🧾 11. Conclusion
SmartObstacleDetector combine Computer Vision, Intelligence Artificielle et synthèse vocale pour créer un assistant de navigation fiable pour les personnes malvoyantes.
L’évolution du projet — de SSD MobileNet à YOLOv8 — montre une progression technologique solide vers un système plus précis, plus rapide et plus réaliste.
Ce projet reflète :
✔ un travail d’équipe efficace
✔ la maîtrise des outils IA modernes
✔ une vraie vision d’assistance réelle