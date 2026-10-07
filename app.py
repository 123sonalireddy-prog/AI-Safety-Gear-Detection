import cv2
import streamlit as st
from ultralytics import YOLO

# Streamlit Page Setup
st.set_page_config(page_title="Real-Time View & ByteTrack Overlay", layout="wide")

# Sidebar - Settings
st.sidebar.title("Settings")
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.50, 0.05)
source_type = st.sidebar.radio("Select Video Source", ("Webcam", "Video File"))

video_source = 0
if source_type == "Video File":
    uploaded_file = st.sidebar.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
        video_source = "temp_video.mp4"

# Load YOLO Model
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # Apni custom 'best.pt' file ka path yahan dein

model = load_model()

# Header & Layout
st.title("Real-Time View & ByteTrack Overlay")
col1, col2 = st.columns([3, 1])

with col1:
    st_frame = st.empty()  # Live feed placeholder

with col2:
    status_placeholder = st.empty()

run_stream = st.checkbox("Start Stream", value=True)

if run_stream:
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        st.error("Error: Camera ya Video Source open nahi ho raha.")
    else:
        while cap.isOpened() and run_stream:
            ret, frame = cap.read()
            if not ret:
                st.warning("Video stream end ho gaya ya frame read karne mein problem hai.")
                break

            # 1. Run YOLO Object Detection with ByteTrack
            results = model.track(
                source=frame, 
                persist=True, 
                tracker="bytetrack.yaml", 
                conf=conf_threshold,
                verbose=False