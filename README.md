# SmartObstacleDetector
Système intelligent d’aide à la navigation pour malvoyants.  
Il utilise la vision par ordinateur pour détecter les obstacles et alerter l’utilisateur en temps réel via des signaux sonores ou vocaux.

🛠️ Technologies utilisées

- Python 3.x  
- OpenCV pour la capture et le traitement d’images/vidéos  
- **YOLOv11n** et **YOLOv8** pré-entraînés pour la détection d’objets  
- **SSD MobileNet** pour une alternative plus légère  
- pyttsx3 / playsound pour générer des alertes vocales ou sonores  
- Flask pour l’interface web locale
  
⚡ Fonctionnalités

- Détection d’obstacles sur images fixes et vidéos en temps réel  
- Alertes sonores ou vocales lorsqu’un obstacle est détecté  
- Paramètres simples pour ajuster le seuil de détection et filtrer les faux positifs  
- Interface web intuitive pour lancer/arrêter la détection et choisir le mode 

# Installation

1. Cloner le projet :  
   ```bash
   git clone <url_du_projet>
   cd SmartObstacleDetecto
# Comment exécuter le projet

1.Démarrer le serveur Flask depuis le dossier principal du projet :

    python server.py


2. Ouvrir un navigateur web et accéder à :

    http://localhost:5000


3. Depuis l’interface web :

  -Sélectionner le mode de détection (YOLOv11n ou SSD MobileNet)

  -Cliquer sur Commencer la détection pour lancer le script correspondant

  -Cliquer sur Arrêter la détection pour arrêter le processus

