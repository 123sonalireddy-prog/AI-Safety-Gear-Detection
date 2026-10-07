Python 3.11.2 (tags/v3.11.2:878ead1, Feb  7 2023, 16:38:35) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import cv2
... from ultralytics import YOLO
... 
... # Model load karein (yolov8n.pt / yolov11n.pt ya aapka custom model)
... model = YOLO("yolov8n.pt")
... 
... # Video source (0 live webcam ke liye ya "video.mp4")
... cap = cv2.VideoCapture("input_video.mp4")
... 
... while cap.isOpened():
...     success, frame = cap.read()
...     if not success:
...         break
... 
...     # Ultralytics ka built-in ByteTrack
...     results = model.track(
...         source=frame,
...         persist=True,             # Frame to frame track ID maintain rakhta hai
...         tracker="bytetrack.yaml", # Built-in ByteTrack config
...         conf=0.25                 # Detection threshold
...     )
... 
...     # Output visualize karein
...     annotated_frame = results[0].plot()
...     cv2.imshow("YOLO + ByteTrack (Built-in)", annotated_frame)
... 
...     if cv2.waitKey(1) & 0xFF == ord("q"):
...         break
... 
... cap.release()
