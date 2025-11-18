🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback
Projet académique – Vision par Ordinateur & Intelligence Artificielle
🧠 Description du Projet
Ce projet consiste à développer un système d’assistance pour personnes malvoyantes, capable de détecter des objets en temps réel à l’aide d’une webcam, puis d’annoncer vocalement les objets détectés.
La solution utilise TensorFlow 2, OpenCV, et un modèle pré-entraîné SSD MobileNet V2, garantissant une exécution rapide et efficace sur des machines standards.
Ce projet a été réalisé dans le cadre d’un projet académique, avec pour objectif de présenter un prototype fonctionnel devant un jury.
🚀 Fonctionnalités principales
🎥 1. Détection d’objets en temps réel
Basée sur le modèle SSD MobileNet V2 (TensorFlow 2)
Détection rapide et précise
Boîtes englobantes et labels affichés à l’écran
🔊 2. Synthèse vocale automatique
Chaque objet détecté est annoncé via voix
Stabilisation de la parole pour éviter les répétitions
Utilisation de pyttsx3 (offline → fonctionne sans internet)
📦 3. Modèle embarqué
Modèle TensorFlow pré-extrait fourni dans le repo
Aucun téléchargement externe nécessaire
Facile à exécuter même pour débutants
💻 4. Exécution simple
Un seul script Python à lancer :
object_detection_speaking.py → détection + voix
object_detection_webcam.py → détection seule
🔧 5. Installation facile
Via un fichier requirements.txt propre et optimisé
Compatible Windows, macOS, Linux
📁 Structure du projet
Blind-Assistance-Object-Detection/
│
├── object_detection_speaking.py        # Détection + Voice Feedback
├── object_detection_webcam.py          # Détection seule
│
├── ssd_mobilenet_v2/                   # Modèle TensorFlow 2 pré-extrait
│   ├── saved_model.pb
│   └── variables/
│       ├── variables.data-00000-of-00001
│       └── variables.index
│
├── requirements.txt                    # Dépendances du projet
└── README.md                           # Documentation
⚙️ Installation
🔹 1. Cloner le projet
git clone https://github.com/<votre-username>/<votre-repo>.git
cd Blind-Assistance-Object-Detection
🔹 2. Créer un environnement virtuel
python3 -m venv blindenv
source blindenv/bin/activate   # macOS / Linux
blindenv\Scripts\activate      # Windows
🔹 3. Installer les dépendances
pip install -r requirements.txt
▶️ Exécution
🔹 Détection + Synthèse vocale (mode principal)
python object_detection_speaking.py
🔹 Détection seule (sans voix)
python object_detection_webcam.py
Quitter
Dans la fenêtre vidéo → appuyer sur la touche Q
🧬 Modèle utilisé
🔹 SSD MobileNet V2 (COCO)
90 classes d’objets (personne, voiture, téléphone, etc.)
Très rapide → idéal pour webcam
Tous les fichiers nécessaires sont déjà inclus dans le projet
🛠️ Technologies utilisées
Technologie	Rôle
TensorFlow 2.15	Détection d’objets
OpenCV	Manipulation vidéo / affichage
NumPy	Traitement des matrices
Pyttsx3	Synthèse vocale offline
Python 3.10+	Langage du projet
🧑‍🏫 Contexte académique
Ce projet a été réalisé dans le cadre d’une évaluation académique visant à :
Manipuler les modèles pré-entraînés TensorFlow
Intégrer une caméra en temps réel
Associer perception visuelle et retour vocal
Développer un prototype fonctionnel d’assistance smart
📌 Travaux futurs
Idées d'améliorations possibles :
📱 Développement d'une application mobile
🧭 Détection de distance + avertissement sonore
🔦 Détection de passage piéton / panneaux routiers
🌦️ Détection d’obstacles en extérieur
🎛 Interface utilisateur améliorée