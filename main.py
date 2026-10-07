import csv
from datetime import datetime
import os
import winsound
import cv2
from ultralytics import YOLO

# Department-wise PPE requirements
DEPARTMENTS = {
    "General Area": [
        "helmet",
        "vest"
    ],
    "Maintenance Area": [
        "helmet",
        "vest",
        "gloves"
    ],
    "Hot Rolling Area": [
        "helmet",
        "vest",
        "gloves",
        "goggles"
    ],
    "Hazardous Area": [
        "helmet",
        "vest",
        "gloves",
        "goggles"
    ]
}


def calculate_compliance(detected_ppe, required_ppe):
    detected_ppe = set(detected_ppe)
    required_ppe = set(required_ppe)

    present = detected_ppe.intersection(required_ppe)

    compliance = (len(present) / len(required_ppe)) * 100

    missing = list(required_ppe - detected_ppe)

    return round(compliance), missing


def entry_decision(compliance, missing_ppe):
    if compliance == 100 and len(missing_ppe) == 0:
        return "ENTRY ALLOWED"
    else:
        return "ENTRY DENIED"


def alert():
    winsound.PlaySound("siren.wav", winsound.SND_FILENAME)


FILE_NAME = "safety_records.csv"


def save_record(department, compliance, status, missing_ppe):
    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Time",
                "Department",
                "Compliance",
                "Status",
                "Missing PPE"
            ])

        now = datetime.now()

        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            department,
            str(compliance) + "%",
            status,
            ", ".join(missing_ppe)
        ])