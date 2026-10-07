AI Safety Gear Detection System

📌 Project Overview

The AI Safety Gear Detection System is an AI-based workplace safety monitoring project designed to detect whether workers are wearing the required Personal Protective Equipment (PPE).

The system uses Python, YOLO, and OpenCV to detect safety equipment such as helmets, safety vests, gloves, and goggles from images or a live camera feed.

The main objective is to improve workplace safety by identifying missing safety gear and providing an immediate compliance status.

🎯 Problem Statement

In industrial environments, workers are required to wear appropriate safety equipment. Manual monitoring of PPE compliance can be difficult, time-consuming, and may not detect violations immediately.

This project provides an automated approach to monitor PPE compliance using computer vision and object detection.

💡 Proposed Solution

The system captures an image or video frame through a camera and uses a YOLO-based object detection model to identify safety equipment.

The detected PPE is then checked according to the requirements of the working area. The system determines whether the worker is compliant or whether any required safety gear is missing.

⚙️ Main Features

- Helmet detection
- Safety vest detection
- Glove detection
- Goggle detection
- PPE compliance checking
- Live camera-based detection
- Image/video-based detection
- Area-specific safety requirements
- Compliance status display
- Alert mechanism for missing safety equipment

🏭 Area-Based PPE Requirements

The system can apply different PPE requirements depending on the working area.

Working Area| Required PPE
General Area| Helmet, Vest
Maintenance Area| Helmet, Vest, Gloves
Hot Rolling Area| Helmet, Vest, Gloves, Goggles
Hazardous Area| Helmet, Vest, Gloves, Goggles

🧠 Technologies Used

- Python
- YOLO
- Ultralytics
- OpenCV
- NumPy
- Computer Vision
- Object Detection

🔄 System Workflow

Camera / Image / Video
          ↓
     Frame Capture
          ↓
     YOLO Detection
          ↓
    PPE Identification
          ↓
   Compliance Checking
          ↓
 Required PPE Present?
       ↙        ↘
     YES         NO
      ↓           ↓
  COMPLIANT     ALERT

📂 Project Structure

AI-Safety-Gear-Detection/
│
├── main.py
├── config.py
├── compliance.py
├── decision.py
├── siren.py
├── requirements.txt
├── README.md
│
├── models/
│   └── model.pt
│
└── screenshots/

🚀 How It Works

1. The system receives an image, video, or live camera feed.
2. YOLO detects the available safety equipment.
3. The detected PPE is compared with the required PPE for the selected area.
4. The compliance module checks whether all required equipment is present.
5. The system displays the safety status.
6. If required PPE is missing, the system can generate an alert.

🔮 Future Scope

- Integration with Raspberry Pi or other edge devices
- IP camera integration
- Real-time industrial monitoring
- Improved detection accuracy
- Automatic incident logging
- Cloud-based monitoring dashboard
- Multiple-camera support
- Advanced alert and notification systems

👩‍💻 Project Purpose

This project demonstrates how Artificial Intelligence and Computer Vision can be applied to improve workplace safety and support preventive safety monitoring in industrial environments.

📜 Note

This project is developed as an academic/prototype project for demonstrating AI-based PPE detection and safety compliance monitoring.
