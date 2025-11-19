# 🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback  
### *Projet académique – Vision par Ordinateur & Intelligence Artificielle*

---

## 🧠 Description du Projet

Ce projet propose un système d’assistance pour personnes malvoyantes capable de :

- détecter des objets en temps réel via webcam,
- annoncer vocalement les objets identifiés,
- afficher les boîtes englobantes grâce à OpenCV.

Il repose sur **TensorFlow 2**, **OpenCV**, et le modèle pré-entraîné **SSD MobileNet V2**.  
Développé dans le cadre d’un **projet académique**, il vise à présenter un prototype fonctionnel devant un jury.

---

## 🚀 Fonctionnalités principales

### 🎥 Détection d’objets en temps réel
- Basée sur **SSD MobileNet V2 – COCO**
- 90 classes d’objets supportées
- Fonctionne en temps réel (selon la machine)

### 🔊 Synthèse vocale automatique
- Annonce vocale de chaque objet détecté
- Anti-répétition intégré (évite les interférences audio)
- Fonctionne entièrement offline (`pyttsx3`)

### 📦 Modèle inclus dans le projet
Le dossier `ssd_mobilenet_v2/` contient :
- `saved_model.pb`
- `variables/`

Aucun téléchargement supplémentaire n’est nécessaire.

### 🖥 Scripts disponibles

| Script | Fonction |
|--------|----------|
| `object_detection_speaking.py` | Détection + annonce vocale |
| `object_detection_webcam.py` | Détection seule |

---

## 📁 Structure du projet

```text
Blind-Assistance-Object-Detection/
│
├── object_detection_speaking.py        # Détection + Voix
├── object_detection_webcam.py          # Détection seule
│
├── ssd_mobilenet_v2/                   # Modèle TensorFlow 2
│   ├── saved_model.pb
│   └── variables/
│       ├── variables.data-00000-of-00001
│       └── variables.index
│
├── requirements.txt                    # Dépendances
└── README.md                           # Documentation
# 🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback  
### *Projet académique – Vision par Ordinateur & Intelligence Artificielle*

---

## 🧠 Description du Projet

Ce projet propose un système d’assistance pour personnes malvoyantes capable de :

- détecter des objets en temps réel via webcam,
- annoncer vocalement les objets identifiés,
- afficher les boîtes englobantes grâce à OpenCV.

Il repose sur **TensorFlow 2**, **OpenCV**, et le modèle pré-entraîné **SSD MobileNet V2**.  
Développé dans le cadre d’un **projet académique**, il vise à présenter un prototype fonctionnel devant un jury.

---

## 🚀 Fonctionnalités principales

### 🎥 Détection d’objets en temps réel
- Basée sur **SSD MobileNet V2 – COCO**
- 90 classes d’objets supportées
- Fonctionne en temps réel (selon la machine)

### 🔊 Synthèse vocale automatique
- Annonce vocale de chaque objet détecté
- Anti-répétition intégré (évite les interférences audio)
- Fonctionne entièrement offline (`pyttsx3`)

### 📦 Modèle inclus dans le projet
Le dossier `ssd_mobilenet_v2/` contient :
- `saved_model.pb`
- `variables/`

Aucun téléchargement supplémentaire n’est nécessaire.

### 🖥 Scripts disponibles

| Script | Fonction |
|--------|----------|
| `object_detection_speaking.py` | Détection + annonce vocale |
| `object_detection_webcam.py` | Détection seule |

---

## 📁 Structure du projet

```text
Blind-Assistance-Object-Detection/
│
├── object_detection_speaking.py        # Détection + Voix
├── object_detection_webcam.py          # Détection seule
│
├── ssd_mobilenet_v2/                   # Modèle TensorFlow 2
│   ├── saved_model.pb
│   └── variables/
│       ├── variables.data-00000-of-00001
│       └── variables.index
│
├── requirements.txt                    # Dépendances
└── README.md                           # Documentation

⚙️ Installation
🔷 1. Cloner le projet
git clone https://github.com/DERRAOUISAFIA/SmartObstacleDetecto.git
cd SmartObstacleDetecto
🔷 2. Créer un environnement virtuel
macOS / Linux
python3 -m venv blindenv
source blindenv/bin/activate
Windows
python -m venv blindenv
blindenv\Scripts\activate
🔷 3. Installer les dépendances
pip install -r requirements.txt
▶️ Exécution
🔊 Détection + Synthèse vocale
python object_detection_speaking.py
🎥 Détection seule (sans voix)
python object_detection_webcam.py
❌ Quitter
Dans la fenêtre vidéo : appuyer sur la touche Q.
🧬 Modèle utilisé
SSD MobileNet V2 – COCO dataset (90 classes)
Très rapide → idéal pour du temps réel
Fonctionne sans GPU (CPU OK)
🛠️ Technologies utilisées
Technologie	Rôle
TensorFlow 2.15	Détection d’objets
OpenCV	Webcam + affichage
NumPy	Traitement numérique
pyttsx3	Synthèse vocale offline
Python 3.10+	Langage
🧑‍🏫 Contexte académique
Ce projet a été réalisé dans le cadre :
d’un module d’intelligence artificielle,
visant l’intégration de modèles pré-entraînés,
la manipulation vidéo en temps réel,
l’assistance intelligente pour malvoyants