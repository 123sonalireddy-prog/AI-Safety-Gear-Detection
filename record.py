import csv
from datetime import datetime
import os

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