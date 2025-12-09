import threading
import time
from collections import defaultdict
import math

class VoiceFeedback:
    """Text-to-speech avec suivi d'objets pour éviter les annonces répétées."""
    
    def __init__(self, cooldown=5.0, frame_width=640, frame_height=480, tracking_threshold=50):
        self.cooldown = cooldown
        self.last_announced = defaultdict(float)
        self.object_positions = {}
        self.object_classes = {}
        self.next_id = 0
        self.tracking_threshold = tracking_threshold
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        self.speech_engine = self._init_speech_engine()
        self.speech_available = self.speech_engine is not None
        
        if self.speech_available:
            print("✓ Synthèse vocale initialisée")
        else:
            print("✗ Synthèse vocale non disponible - mode texte seulement")
       #file de parole et un thread dédié sont créés pour gérer les annonces vocales en arrière-plan 
        self.speech_queue = []
        self.lock = threading.Lock()
        self.running = True
        
        if self.speech_available:
            self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.speech_thread.start()
        else:
            self.speech_thread = None
        
        print(f"VoiceFeedback initialisé - Cooldown: {cooldown}s, Suivi: {tracking_threshold}px")
    
    def _init_speech_engine(self):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            voices = engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if 'french' in voice.name.lower() or 'france' in voice.name.lower() or 'français' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        print(f"  Voix française trouvée: {voice.name}")
                        break
                return engine
            else:
                return None
        except Exception as e:
            print(f"  Erreur initialisation pyttsx3: {e}")
            try:
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                print("  Utilisation de SAPI Windows")
                return speaker
            except:
                print("  SAPI Windows non disponible")
                return None
  #Fonction exécutée en arrière-plan. Vérifie toutes les 0,1 s s’il y a un texte à prononcer utilise _speak_text() pour prononcer le texte.  
    def _speech_worker(self):
        while self.running:
            with self.lock:
                if self.speech_queue:
                    text = self.speech_queue.pop(0)
                else:
                    text = None
            if text:
                try:
                    self._speak_text(text)
                    print(f"🔊 {text}")
                except Exception as e:
                    print(f"Erreur parole: {e} - {text}")
            time.sleep(0.1)
    #Si synthèse vocale indisponible elle affiche le texte dans le terminal.
    def _speak_text(self, text):
        if not self.speech_available:
            print(f"[VOIX] {text}")
            return
        try:
            if hasattr(self.speech_engine, 'say'):
                self.speech_engine.say(text)
                self.speech_engine.runAndWait()
            elif hasattr(self.speech_engine, 'Speak'):
                self.speech_engine.Speak(text)
        except Exception as e:
            print(f"Erreur lors de la parole: {e} - [TEXTE] {text}")
    
    def _calculate_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return (x1 + x2) / 2.0, (y1 + y2) / 2.0
    
    def _find_closest_object(self, center_x, center_y, current_class=None):
        closest_id = None
        min_distance = float('inf')
        for obj_id, (prev_x, prev_y) in self.object_positions.items():
            if current_class is not None and obj_id in self.object_classes:
                if self.object_classes[obj_id] != current_class:
                    continue
            distance = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
            if distance < min_distance and distance < self.tracking_threshold:
                min_distance = distance
                closest_id = obj_id
        return closest_id
    
    def _get_position_text(self, center_x):
        if center_x < self.frame_width * 0.33:
            return "à gauche"
        elif center_x > self.frame_width * 0.66:
            return "à droite"
        else:
            return "devant"
    
    def _translate_class_to_french(self, class_name):
        translations = {
        'person': 'personne',
        'bicycle': 'vélo',
        'car': 'voiture',
        'motorcycle': 'moto',
        'airplane': 'avion',
        'bus': 'bus',
        'train': 'train',
        'truck': 'camion',
        'boat': 'bateau',
        'traffic light': 'feu de circulation',
        'fire hydrant': 'borne incendie',
        'stop sign': 'panneau stop',
        'parking meter': 'parcmètre',
        'bench': 'banc',
        'bird': 'oiseau',
        'cat': 'chat',
        'dog': 'chien',
        'horse': 'cheval',
        'sheep': 'mouton',
        'cow': 'vache',
        'elephant': 'éléphant',
        'bear': 'ours',
        'zebra': 'zèbre',
        'giraffe': 'girafe',
        'backpack': 'sac à dos',
        'umbrella': 'parapluie',
        'handbag': 'sac à main',
        'tie': 'cravate',
        'suitcase': 'valise',
        'frisbee': 'frisbee',
        'skis': 'skis',
        'snowboard': 'planche de snowboard',
        'sports ball': 'balle de sport',
        'kite': 'cerf-volant',
        'baseball bat': 'batte de baseball',
        'baseball glove': 'gant de baseball',
        'skateboard': 'skateboard',
        'surfboard': 'planche de surf',
        'tennis racket': 'raquette de tennis',
        'bottle': 'bouteille',
        'wine glass': 'verre à vin',
        'cup': 'tasse',
        'fork': 'fourchette',
        'knife': 'couteau',
        'spoon': 'cuillère',
        'bowl': 'bol',
        'banana': 'banane',
        'apple': 'pomme',
        'sandwich': 'sandwich',
        'orange': 'orange',
        'broccoli': 'brocoli',
        'carrot': 'carotte',
        'hot dog': 'hot-dog',
        'pizza': 'pizza',
        'donut': 'donut',
        'cake': 'gâteau',
        'chair': 'chaise',
        'couch': 'canapé',
        'potted plant': 'plante en pot',
        'bed': 'lit',
        'dining table': 'table',
        'toilet': 'toilettes',
        'tv': 'télévision',
        'laptop': 'ordinateur portable',
        'mouse': 'souris',
        'remote': 'télécommande',
        'keyboard': 'clavier',
        'cell phone': 'téléphone',
        'microwave': 'micro-ondes',
        'oven': 'four',
        'toaster': 'grille-pain',
        'sink': 'évier',
        'refrigerator': 'réfrigérateur',
        'book': 'livre',
        'clock': 'horloge',
        'vase': 'vase',
        'scissors': 'ciseaux',
        'teddy bear': 'ours en peluche',
        'hair drier': 'sèche-cheveux',
        'toothbrush': 'brosse à dents',
        'hair brush': 'brosse à cheveux'
    }
        return translations.get(class_name.strip().lower(), class_name)
    
    def announce_object(self, class_name, distance_label=None, bbox=None, force=False):
        current_time = time.time()
        if bbox is not None:
            center_x, center_y = self._calculate_center(bbox)
            obj_id = self._find_closest_object(center_x, center_y, class_name)
            if obj_id is None:
                obj_id = self.next_id
                self.next_id += 1
            self.object_positions[obj_id] = (center_x, center_y)
            self.object_classes[obj_id] = class_name
            key = f"{class_name}_{obj_id}"
        else:
            key = f"{class_name}_{distance_label}"
        
        if not force and (current_time - self.last_announced.get(key, 0)) < self.cooldown:
            return
        
        self.last_announced[key] = current_time
        class_fr = self._translate_class_to_french(class_name)
        
        if distance_label == "Inconnue":
            if bbox is not None:
                center_x, _ = self._calculate_center(bbox)
                position = self._get_position_text(center_x)
                announcement = f"{class_fr} {position}"
            else:
                announcement = f"{class_fr}"
        else:
            if bbox is not None:
                center_x, _ = self._calculate_center(bbox)
                position = self._get_position_text(center_x)
                announcement = f"{class_fr} {distance_label.lower()} {position}"
            else:
                announcement = f"{class_fr} {distance_label.lower()}"
        
        with self.lock:
            self.speech_queue.append(announcement)
    
    def announce_summary(self, object_counts, include_positions=False, detected_objects=None):
        if not object_counts:
            return
        if include_positions and detected_objects:
            announcements = []
            for obj_info in detected_objects[:3]:
                class_name = obj_info.get('class', 'objet')
                distance_label = obj_info.get('distance_label', '')
                bbox = obj_info.get('bbox')
                class_fr = self._translate_class_to_french(class_name)
                
                if bbox is not None: 
                    center_x, _ = self._calculate_center(bbox)
                    position = self._get_position_text(center_x)
                    if distance_label and distance_label != "Inconnue":
                        announcements.append(f"{class_fr} {distance_label.lower()} {position}")
                    else:
                        announcements.append(f"{class_fr} {position}")
            
            if announcements:
                summary = "Je vois " + ", ".join(announcements)
                with self.lock:
                    self.speech_queue.append(summary)
        else:
            parts = []
            for cls, count in list(object_counts.items())[:4]:
                cls_fr = self._translate_class_to_french(cls)
                if count == 1:
                    parts.append(f"une {cls_fr}")
                else:
                    parts.append(f"{count} {cls_fr}")
            if parts:
                summary = "Je vois " + ", ".join(parts)
                with self.lock:
                    self.speech_queue.append(summary)
    
    def clear_tracking(self):
        self.object_positions.clear()
        self.object_classes.clear()
        self.next_id = 0
        print("Suivi des objets réinitialisé")
    
    def update_frame_size(self, width, height):
        self.frame_width = width
        self.frame_height = height
    
    def cleanup(self):
        self.running = False
        if self.speech_thread and self.speech_thread.is_alive():
            self.speech_thread.join(timeout=1.0)
        print("VoiceFeedback nettoyé")
