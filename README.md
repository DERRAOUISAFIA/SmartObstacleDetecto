# 🌟 Blind Assistance – Real-Time Object Detection with Voice Feedback
### *Projet académique – Vision par Ordinateur & Intelligence Artificielle*

---

## 🧠 Description du Projet

Ce projet propose un système d’assistance pour personnes malvoyantes, capable de :

- détecter des objets en temps réel via une webcam,
- annoncer vocalement les éléments identifiés,
- afficher les objets détectés grâce à OpenCV.

Il utilise **TensorFlow 2**, **OpenCV**, et un modèle pré-entraîné **SSD MobileNet V2**, optimisé pour la rapidité.  
Ce projet a été développé dans un cadre **académique**, afin de présenter un prototype fonctionnel devant un jury.

---

## 🚀 Fonctionnalités principales

### 🎥 Détection d’objets en temps réel
- Basée sur **SSD MobileNet V2**  
- 90 classes COCO supportées  
- Résultats rapides (idéal webcam)

### 🔊 Synthèse vocale automatique
- Annonce l’objet détecté (ex: “person ahead”)  
- Système anti-répétition intégré (évite les boucles de voix)

### 📦 Modèle embarqué
- Modèle TensorFlow inclus dans le dossier `ssd_mobilenet_v2/`
- Fonctionne offline
- Exécution immédiate sans téléchargement externe

### 🖥 Scripts disponibles
- `object_detection_speaking.py` → détection + voix  
- `object_detection_webcam.py` → détection seule  

---

## 📁 Structure du projet

