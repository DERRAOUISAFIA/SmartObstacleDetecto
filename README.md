🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback
Projet académique – Vision par Ordinateur & Intelligence Artificielle
🧠 Description du Projet
Ce projet propose un système d’assistance pour personnes malvoyantes, capable de :
détecter des objets en temps réel via une webcam,
annoncer vocalement les objets identifiés,
afficher les objets détectés grâce à OpenCV.
La solution repose sur TensorFlow 2, OpenCV, et un modèle pré-entraîné SSD MobileNet V2, optimisé pour la rapidité et la précision.
Ce projet a été réalisé dans un cadre académique, dans le but de présenter un prototype fonctionnel devant un jury.
🚀 Fonctionnalités principales
🎥 Détection d’objets en temps réel
Basée sur SSD MobileNet V2 COCO (90 classes : personne, voiture, téléphone…)
Très rapide → idéale pour webcam
Boîtes englobantes et labels affichés à l’écran
🔊 Synthèse vocale automatique
Lecture vocale des objets détectés
Fonction anti-répétition intégrée
Fonctionne entièrement offline via pyttsx3
📦 Modèle embarqué
Modèle TensorFlow 2 inclus dans ssd_mobilenet_v2/
Aucune installation externe nécessaire
🖥️ Scripts inclus
object_detection_speaking.py → détection + voix
object_detection_webcam.py → détection seule
📁 Structure du projet
Blind-Assistance-Object-Detection/
│
├── object_detection_speaking.py
├── object_detection_webcam.py
│
├── ssd_mobilenet_v2/
│   ├── saved_model.pb
│   └── variables/
│       ├── variables.data-00000-of-00001
│       └── variables.index
│
├── requirements.txt
└── README.md
⚙️ Installation
🔹 1. Cloner le projet
git clone https://github.com/<votre-username>/<votre-repo>.git
cd Blind-Assistance-Object-Detection
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
Dans la fenêtre vidéo, appuyer sur Q.
🧬 Modèle utilisé
🔹 SSD MobileNet V2 – COCO dataset
90 classes d’objets supportées
Très rapide → approprié pour traitement temps réel
Modèle complet inclus directement dans le repo
Fonctionne sur CPU (aucun GPU nécessaire)
🛠️ Technologies utilisées
Technologie	Rôle
TensorFlow 2.15	Détection d’objets
OpenCV	Webcam & affichage vidéo
NumPy	Traitement d’images/matrices
pyttsx3	Synthèse vocale offline
Python 3.10+	Langage du projet
🧑‍🏫 Contexte académique
Ce projet a été réalisé dans le cadre :
d’un module académique sur l’intelligence artificielle,
visant l’intégration de modèles pré-entraînés TensorFlow,
la manipulation d’une webcam en temps réel,
et la création d’un prototype d’assistance pour malvoyants.
📌 Travaux futurs
📱 Développement d’une application mobile
🧭 Détection de distance / alertes (ultrasons / stéréo-vision)
🔦 Détection de passages piétons
⚠️ Détection d’obstacles extérieurs
🎛 Interface utilisateur améliorée
📄 Licence
Ce projet est publié sous licence MIT.