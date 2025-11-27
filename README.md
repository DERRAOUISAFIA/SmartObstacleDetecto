SmartObstacleDetector — Obstacle Detection Assistant for Visually Impaired Users
1. Introduction
SmartObstacleDetector is a real-time obstacle detection system designed to assist visually impaired users by identifying objects, estimating their distance and direction, and optionally providing intelligent voice alerts.
The system uses TensorFlow + SSD MobileNet V2, supports webcam input, and includes modules for image detection, real-time video analysis, audio alerts, and model optimization.
2. Features
2.1 Real-Time Object Detection
SSD MobileNet V2 pretrained on COCO dataset
Detects up to 90 object classes
Works on standard webcams
Real-time bounding box rendering
2.2 Voice Alerts (Final Prototype)
Offline text-to-speech using pyttsx3
Direction detection: left / center / right
Distance estimation: near / far
Anti-repetition with cooldown logic
Natural-sounding French alerts
2.3 Advanced Video Module
Real-time distance estimation using focal length
Color-coded bounding boxes (green/orange/red)
FPS tracking
Screenshot & video recording options
2.4 Image Detection Module
Runs object detection on static images
Useful for debugging, testing, and validation
2.5 Optimization Module
Threshold and confidence tuning
Performance evaluation
Model comparison
3. Team Responsibilities
Member	File	Responsibilities
Member 1 — Image Detection	src/images/detection_image.py	Load model, detect objects on images, draw bounding boxes
Member 2 — Webcam Detection + Distance + FPS	src/webcam/test.py	Real-time detection, distance estimation, FPS tracking
Member 3 — Voice Alerts (Final Prototype)	src/alerts/object_detection_speaking.py	Intelligent voice alerts, direction & distance logic, cooldown
Member 4 — Optimization	src/optimization/optimization.py	Threshold tuning, performance evaluation, testing setups
4. Project Structure
```
SmartObstacleDetector/
│
├── src/
│   ├── images/
│   │    └── detection_image.py
│   ├── webcam/
│   │    └── test.py
│   ├── alerts/
│   │    └── object_detection_speaking.py
│   ├── optimization/
│   │    └── optimization.py
│   └── utils/
│        └── common.py (optional)
│
├── ssd_mobilenet_v2/
│   ├── saved_model.pb
│   └── variables/
│
├── requirements.txt
└── README.md
```
5. Installation

Step 1 — Clone the repository
```
git clone https://github.com/your-repo/SmartObstacleDetector.git
cd SmartObstacleDetector
```
Step 2 — Create a virtual environment
macOS / Linux
```
python3 -m venv venv
source venv/bin/activate
```
Windows
```
python -m venv venv
venv\Scripts\activate
```
Step 3 — Install dependencies
```
pip install -r requirements.txt
```
6. Running the Project
Final Prototype (Voice Alerts)
```
python src/alerts/object_detection_speaking.py
```
Image Detection Module
```
python src/images/detection_image.py
```
Webcam Detection + Distance + FPS
```
python src/webcam/test.py
```
Optimization Module
```
python src/optimization/optimization.py
```
7. Model Used
    SSD MobileNet V2 (COCO)
    90 object categories
    Optimized for real-time inference
    Pretrained model stored in:
        ssd_mobilenet_v2/
8. Technologies Used
| Technology       | Purpose                 |
| ---------------- | ----------------------- |
| **TensorFlow 2** | Object detection        |
| **OpenCV**       | Webcam/video processing |
| **pyttsx3**      | Offline text-to-speech  |
| **NumPy**        | Numerical operations    |
| **Python 3.10+** | Programming language    |

9. Suggested Demo Flow (For Jury Presentation)
        Introduction (Member 4)
        Image detection demo (Member 1)
        Real-time webcam detection + distance estimation (Member 2)
        Final prototype with voice alerts (Member 3)
        Conclusion & future improvements (Member 4)
10. Future Improvements
Mobile app version
Staircase & pothole detection
Ultrasonic/LiDAR fusion
GPS navigation integration
Haptic vibration feedback
Wearable device prototype
12. Conclusion
This project demonstrates an effective assistive technology prototype by combining computer vision, real-time processing, distance estimation, and intelligent voice feedback to improve navigation for visually impaired users.
It highlights strong teamwork and a practical understanding of AI systems.
