import os
import cv2
from ultralytics import YOLO

# 1. Updated ByteTrack Config (Added missing 'fuse_score')
yaml_content = """
tracker_type: bytetrack
track_high_thresh: 0.5
track_low_thresh: 0.1
new_track_thresh: 0.6
track_buffer: 30
match_thresh: 0.8
fuse_score: True         # Fixes AttributeError: fuse_score
"""

config_file_path = "custom_bytetrack.yaml"
with open(config_file_path, "w") as f:
    f.write(yaml_content.strip())

# 2. Model Load Karein
model = YOLO("yolov8n.pt") 

# 3. Video Source (0 for webcam, or "input_video.mp4")
video_source = 0  
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print(f"[ERROR] Could not open video source: {video_source}")
    exit()

print("[INFO] ByteTrack Running... Press 'q' to quit.")

# 4. Tracking Loop
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model.track(
        source=frame,
        persist=True,
        tracker=config_file_path,
        conf=0.25
    )

    annotated_frame = results[0].plot()
    cv2.imshow("YOLO + ByteTrack", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()