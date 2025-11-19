# 🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback  
### *Projet académique – Vision par Ordinateur & Intelligence Artificielle*

---

## 🧠 Description du Projet

Ce projet propose un système d’assistance pour personnes malvoyantes capable de :

- détecter des objets en temps réel via webcam,  
- annoncer vocalement les objets détectés,  
- afficher les boîtes englobantes via OpenCV.

La solution repose sur **TensorFlow 2**, **OpenCV**, et un modèle pré-entraîné **SSD MobileNet V2**, optimisé pour la rapidité.  
Ce projet est réalisé dans le cadre d’un **projet académique** afin de présenter un prototype fonctionnel devant un jury.

---

## 🚀 Fonctionnalités principales

### 🎥 Détection d’objets en temps réel
- Basée sur **SSD MobileNet V2 (COCO – 90 classes)**  
- Résultats rapides → idéal pour webcam  
- Affichage en temps réel (bounding boxes + labels)

### 🔊 Synthèse vocale automatique
- Annonce de l’objet détecté (ex : *“person ahead”*)  
- Système anti-répétition pour éviter la surcharge vocale  
- Fonctionne **offline** via `pyttsx3`

### 📦 Modèle embarqué
- Le modèle TensorFlow est déjà inclus dans `ssd_mobilenet_v2/`  
- Aucun téléchargement supplémentaire nécessaire

### 🖥 Scripts disponibles
- `object_detection_speaking.py` → détection + voix  
- `object_detection_webcam.py` → détection uniquement  

---

## 📁 Structure du projet

Blind-Assistance-Object-Detection/
│
├── object_detection_speaking.py # Détection + retour vocal
├── object_detection_webcam.py # Détection seule
│
├── ssd_mobilenet_v2/ # Modèle TensorFlow 2 inclus
│ ├── saved_model.pb
│ └── variables/
│ ├── variables.data-00000-of-00001
│ └── variables.index
│
├── requirements.txt # Dépendances
└── README.md # Documentation

---

## ⚙️ Installation

### 🔹 1. Cloner le projet
```bash
git clone https://github.com/DERRAOUISAFIA/SmartObstacleDetecto.git
cd SmartObstacleDetecto
🔹 2. Créer un environnement virtuel
macOS / Linux :
python3 -m venv blindenv
source blindenv/bin/activate
Windows :
python -m venv blindenv
blindenv\Scripts\activate
🔹 3. Installer les dépendances
pip install -r requirements.txt
▶️ Exécution
🔊 Détection + synthèse vocale
python object_detection_speaking.py
🎥 Détection seule
python object_detection_webcam.py
❌ Quitter
Dans la fenêtre vidéo : appuyer sur la touche Q.
🧬 Modèle utilisé
SSD MobileNet V2 – COCO dataset (90 classes)
Très rapide → idéal pour temps réel
Modèle complet inclus dans le dépôt
🛠️ Technologies utilisées
Technologie	Rôle
TensorFlow 2.15	Détection d’objets
OpenCV	Webcam & affichage vidéo
NumPy	Traitement des matrices
pyttsx3	Synthèse vocale locale (offline)
Python 3.10+	Langage du projet
🧑‍🏫 Contexte académique
Ce projet a été réalisé dans le cadre d’un module visant :
l'utilisation de modèles pré-entraînés TensorFlow,
la manipulation d'une webcam en temps réel,
l’intégration d’une synthèse vocale,
la création d’un prototype d’assistance pour malvoyants.
📌 Travaux futurs
📱 Application mobile
🧭 Détection de distance (ultrasons / stéréo-vision)
🔦 Détection de passages piétons
⚠️ Détection d’obstacles extérieurs
🎛 Interface utilisateur améliorée