AI Safety Gear & Fire Detection System

 Project Overview

The AI Safety Gear & Fire Detection System is an AI-based workplace safety monitoring prototype designed to improve safety in industrial environments.

The system uses Python, YOLO, and OpenCV to detect required Personal Protective Equipment (PPE), such as helmets, safety vests, gloves, and goggles, and to identify fire-related hazards through camera-based monitoring.

The system checks PPE compliance according to different working areas and helps identify unsafe conditions at an early stage.

 Problem Statement

In industrial environments, workers are required to follow specific safety rules and wear appropriate protective equipment. Manual monitoring can be difficult and may not identify unsafe situations immediately.

Fire and other hazardous conditions can also create serious risks if they are not detected quickly.

This project provides an automated computer-vision-based approach for PPE compliance monitoring and fire hazard detection.

Proposed Solution

The system receives images, videos, or live camera frames and uses a YOLO-based object detection model to identify safety equipment and fire-related hazards.

The detected PPE is compared with the safety requirements of the selected working area. The system then determines whether the worker is compliant or whether required safety equipment is missing.

If a fire-related hazard is detected, the system can indicate the situation as unsafe and generate an alert mechanism.

 Main Features

- Helmet detection
- Safety vest detection
- Glove detection
- Goggle detection
- PPE compliance checking
- Area-based safety requirements
- Hazardous area monitoring
- Fire detection
- Live camera-based monitoring
- Image and video-based detection
- Safety status display
- Alert mechanism for unsafe conditions

 Area-Based PPE Requirements

Working Area| Required PPE
General Area| Helmet, Vest
Maintenance Area| Helmet, Vest, Gloves
Hot Rolling Area| Helmet, Vest, Gloves, Goggles
Hazardous Area| Helmet, Vest, Gloves, Goggles

Technologies Used

- Python
- YOLO
- Ultralytics
- OpenCV
- NumPy
- Computer Vision
- Object Detection

System Workflow

Camera / Image / Video
↓
Frame Capture
↓
YOLO Object Detection
↓
PPE & Fire Detection
↓
Safety Compliance Checking
↓
Safety Status / Alert

How It Works

1. The system receives an image, video, or live camera feed.
2. YOLO detects PPE and fire-related objects.
3. The detected PPE is compared with the required PPE for the selected working area.
4. The compliance module checks whether all required equipment is present.
5. The system displays the safety status.
6. If required PPE is missing or a fire hazard is detected, the system indicates an unsafe condition.

 Future Scope

- Raspberry Pi or edge-device integration
- IP camera integration
- Real-time industrial monitoring
- Improved detection accuracy
- Automatic incident logging
- Multiple-camera monitoring
- Advanced alert and notification system
- Cloud-based safety monitoring

 Project Purpose

This project demonstrates how Artificial Intelligence and Computer Vision can be used for preventive workplace safety monitoring by combining PPE compliance detection and fire hazard detection in a single system.

 Note

This project is developed as an academic prototype to demonstrate AI-based safety gear detection, workplace safety compliance monitoring, and fire hazard detection.
