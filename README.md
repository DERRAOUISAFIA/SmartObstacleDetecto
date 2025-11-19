🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback
Projet académique – Vision par Ordinateur & Intelligence Artificielle
🧠 Description du projet
Ce projet propose un système d’assistance intelligent pour personnes malvoyantes, capable de :
🎥 détecter des objets en temps réel via webcam,
🔊 annoncer vocalement les objets identifiés,
🖼️ afficher les objets détectés grâce à OpenCV.
Il s’appuie sur TensorFlow 2, OpenCV, SSD MobileNet V2, garantissant rapidité et exécution en temps réel.
Ce projet a été développé dans le cadre d’un projet académique et sera présenté devant un jury.
🚀 Fonctionnalités principales
🎥 Détection d’objets en temps réel
Modèle : SSD MobileNet V2 (COCO dataset – 90 classes)
Idéal pour webcam (rapide et léger)
Bounding boxes + pourcentage de confiance
🔊 Synthèse vocale automatique
Annonce vocale des objets détectés
Système anti-répétition (évite d’entendre “person… person… person”)
📦 Modèle embarqué
Modèle TensorFlow fourni dans : ssd_mobilenet_v2/
Fonctionnement entièrement offline
Aucun téléchargement externe nécessaire
🖥 Scripts disponibles
Fichier	Fonction
object_detection_speaking.py	Détection + Voix
object_detection_webcam.py	Détection seule
📁 Structure du projet
Blind-Assistance-Object-Detection/
│
├── object_detection_speaking.py       # Détection + voix
├── object_detection_webcam.py         # Détection seule
│
├── ssd_mobilenet_v2/                  # Modèle TensorFlow
│   ├── saved_model.pb
│   └── variables/
│       ├── variables.data-00000-of-00001
│       └── variables.index
│
├── requirements.txt                   # Dépendances Python
└── README.md                          # Documentation
⚙️ Installation
🔹 1. Cloner le projet
git clone https://github.com/DERRAOUISAFIA/SmartObstacleDetecto.git
cd SmartObstacleDetecto
🔹 2. Créer un environnement virtuel
macOS / Linux
python3 -m venv blindenv
source blindenv/bin/activate
Windows
python -m venv blindenv
blindenv\Scripts\activate
🔹 3. Installer les dépendances
pip install -r requirements.txt
▶️ Exécution
🔊 Mode principal : Détection + voix
python object_detection_speaking.py
🎥 Mode détection seule
python object_detection_webcam.py
❌ Quitter
Dans la fenêtre vidéo : appuyer sur la touche Q
🧬 Modèle utilisé
SSD MobileNet V2 – COCO dataset
90 classes : personne, voiture, téléphone, bouteille, chat, etc.
Très rapide → idéal webcam
Modèle complet déjà inclus dans le projet
🛠 Technologies utilisées
Technologie	Rôle
TensorFlow 2.15	Détection d’objets
OpenCV	Webcam & affichage vidéo
NumPy	Traitement d’images
pyttsx3	Synthèse vocale (offline)
Python 3.10+	Langage du projet
🧑‍🏫 Contexte académique
Ce projet a été réalisé pour :
appliquer la vision par ordinateur en temps réel
utiliser des modèles pré-entraînés TensorFlow
développer un prototype d’assistance pour malvoyants
combiner perception visuelle + feedback vocal
📌 Travaux futurs possibles
📱 Développement d’une app mobile
🧭 Détection de distance + alertes sonores
🔦 Détection de passages piétons
🌦️ Adaptation pour usage extérieur
🤖 Amélioration du modèle (vitesses / stéréo-vision)