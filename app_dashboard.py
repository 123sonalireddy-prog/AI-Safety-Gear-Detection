import os
import cv2
import winsound
import numpy as np
import pandas as pd
import streamlit as st
from ultralytics import YOLO

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Workplace Safety & Gate Compliance System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Workplace Safety & Gate Entry Compliance System")

# ---------------------------------------------------------
# 2. ByteTrack Configuration Generator
# ---------------------------------------------------------
st.sidebar.header("⚙️ ByteTrack Parameters")
enable_bytetrack = st.sidebar.checkbox("Enable ByteTrack Object Tracking", value=True)

track_high_thresh = st.sidebar.slider("Track High Threshold", 0.1, 1.0, 0.5)
track_low_thresh = st.sidebar.slider("Track Low Threshold", 0.1, 1.0, 0.1)
new_track_thresh = st.sidebar.slider("New Track Threshold", 0.1, 1.0, 0.6)
track_buffer = st.sidebar.slider("Track Buffer (Frames)", 10, 100, 30)

yaml_content = f"""
tracker_type: bytetrack
track_high_thresh: {track_high_thresh}
track_low_thresh: {track_low_thresh}
new_track_thresh: {new_track_thresh}
track_buffer: {track_buffer}
match_thresh: 0.8
fuse_score: True
"""

config_file_path = "custom_bytetrack.yaml"
with open(config_file_path, "w") as f:
    f.write(yaml_content.strip())

# ---------------------------------------------------------
# 3. Main Control Panel
# ---------------------------------------------------------
st.sidebar.header("⚙️ System Controls")

default_model = "best.pt" if os.path.exists("best.pt") else "yolov8n.pt"
model_path = st.sidebar.text_input("YOLO Model Path", default_model)

source_type = st.sidebar.radio("Select Input Mode", ["🖼️ Upload Image", "📹 Webcam", "🎬 Video File"])

uploaded_image = None
video_input = None

if source_type == "🖼️ Upload Image":
    uploaded_image = st.sidebar.file_uploader("Upload Image for Inspection", type=["jpg", "jpeg", "png", "bmp"])
elif source_type == "📹 Webcam":
    cam_index = st.sidebar.selectbox("Camera Source Index", [0, 1, 2], index=0)
    video_input = cam_index
else:
    video_input = st.sidebar.text_input("Video File Path", "input_video.mp4")

conf_threshold = st.sidebar.slider("Detection Confidence", 0.1, 1.0, 0.35)
enable_siren = st.sidebar.checkbox("Enable Warning Siren on Violation", value=False)

run_system = st.sidebar.checkbox("🚀 Start Monitoring / Processing", value=False)

# ---------------------------------------------------------
# 4. Gate Status Banner & Metrics
# ---------------------------------------------------------
gate_banner = st.empty()

col1, col2, col3, col4 = st.columns(4)
metric_tracks = col1.metric("Total Detections / Tracks", "0")
metric_compliant = col2.metric("Compliant Count", "0")
metric_violations = col3.metric("Violations Detected", "0")
metric_gate = col4.metric("Gate Status", "CLOSED 🔴")

st.markdown("---")

gate_banner.info("🔒 System Standby - Gate Closed")

# ---------------------------------------------------------
# 5. Multi-Tab Display Layout
# ---------------------------------------------------------
tab_feed, tab_logs, tab_settings = st.tabs(["📹 Main Feed & Overlay", "📊 Compliance Analytics & Logs", "⚙️ System Parameters"])

with tab_feed:
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("Real-Time View & ByteTrack Overlay")
        st_frame = st.empty()
    with right_col:
        st.subheader("Live Event Stream")
        log_area = st.empty()

with tab_logs:
    st.subheader("📋 Session Violation Records")
    table_placeholder = st.empty()

with tab_settings:
    st.subheader("🛠️ Active System Configurations")
    st.json({
        "Model Path": model_path,
        "Input Mode": source_type,
        "Detection Confidence": conf_threshold,
        "ByteTrack Active": enable_bytetrack,
        "Audio Siren Alert": "Enabled" if enable_siren else "Disabled"
    })

# ---------------------------------------------------------
# 6. Model Processing Loop
# ---------------------------------------------------------
if run_system:
    try:
        model = YOLO(model_path)
    except Exception as e:
        st.error(f"Model load nahi ho paya: {e}")
        st.stop()

    def is_safe_ppe(name):
        name = name.lower()
        if any(k in name for k in ["no-", "without", "no_", "contraband"]):
            return False
        return any(k in name for k in ["helmet", "vest", "hard-hat", "hardhat", "gloves", "mask", "safety"])

    # -----------------------------------------------------
    # MODE 1: Image Processing Logic
    # -----------------------------------------------------
    if source_type == "🖼️ Upload Image":
        if uploaded_image is not None:
            file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)

            results = model.predict(source=img, conf=conf_threshold)
            
            event_logs = []
            log_records = []
            has_ppe = False
            has_violation = False
            total_objs = 0
            compliant_cnt = 0
            violation_cnt = 0

            if results[0].boxes is not None and len(results[0].boxes) > 0:
                class_ids = results[0].boxes.cls.int().cpu().tolist()
                total_objs = len(class_ids)

                for idx, cls_id in enumerate(class_ids):
                    class_name = model.names[cls_id].lower()

                    if is_safe_ppe(class_name):
                        has_ppe = True
                        compliant_cnt += 1
                    else:
                        has_violation = True
                        violation_cnt += 1
                        msg = f"⚠️ DENIED: Item #{idx+1} detected as {class_name.upper()}"
                        event_logs.append(msg)
                        log_records.append({"Item Index": idx+1, "Detection": class_name.upper(), "Access Status": "DENIED"})

            metric_tracks.metric("Total Detections", total_objs)
            metric_compliant.metric("Compliant Count", compliant_cnt)
            metric_violations.metric("Violations Detected", violation_cnt)

            if total_objs == 0:
                metric_gate.metric("Gate Status", "CLOSED 🔴")
                gate_banner.info("🔒 Gate Status: CLOSED (No Detections)")
            elif has_violation or not has_ppe:
                metric_gate.metric("Gate Status", "DENIED ❌")
                gate_banner.error("⛔ ACCESS DENIED! PPE Kit Missing or Safety Violation Detected!")
                if enable_siren:
                    winsound.Beep(1200, 250)
            else:
                metric_gate.metric("Gate Status", "ALLOWED 🟢")
                gate_banner.success("✅ ACCESS ALLOWED! All Safety Compliances Met.")

            annotated_img = results[0].plot()
            annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
            st_frame.image(annotated_img, channels="RGB", use_container_width=True)

            log_text = "\n".join(event_logs) if event_logs else ("✅ Access Granted" if (has_ppe and not has_violation) else "❌ Access Denied: PPE Missing")
            log_area.code(log_text, language="text")

            if log_records:
                table_placeholder.dataframe(pd.DataFrame(log_records), use_container_width=True)
        else:
            st.info("Sidebar me image upload karein.")

    # -----------------------------------------------------
    # MODE 2 & 3: Webcam & Video Stream Tracking Logic
    # -----------------------------------------------------
    else:
        cap = None
        if isinstance(video_input, int):
            cap = cv2.VideoCapture(video_input, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap = cv2.VideoCapture(video_input)
            if not cap.isOpened() and video_input != 0:
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(video_input)

        if cap is None or not cap.isOpened():
            st.error(f"Source access nahi ho paraha hai ({video_input}). Check index or file path.")
            st.stop()

        unique_tracks = set()
        compliant_tracks = set()
        violation_tracks = set()
        event_logs = []
        log_records = []

        while cap.isOpened() and run_system:
            success, frame = cap.read()
            if not success:
                st.warning("Frame read nahi hua ya video end ho gayi.")
                break

            if enable_bytetrack:
                results = model.track(source=frame, persist=True, tracker=config_file_path, conf=conf_threshold)
            else:
                results = model.track(source=frame, persist=True, conf=conf_threshold)

            has_active_ppe = False
            has_active_violation = False
            active_objects_in_frame = False

            if results[0].boxes is not None and len(results[0].boxes) > 0:
                active_objects_in_frame = True
                class_ids = results[0].boxes.cls.int().cpu().tolist()
                
                track_ids = results[0].boxes.id.int().cpu().tolist() if results[0].boxes.id is not None else list(range(len(class_ids)))

                for track_id, cls_id in zip(track_ids, class_ids):
                    class_name = model.names[cls_id].lower()
                    unique_tracks.add(track_id)

                    if is_safe_ppe(class_name):
                        has_active_ppe = True
                        compliant_tracks.add(track_id)
                    else:
                        has_active_violation = True
                        violation_tracks.add(track_id)
                        
                        msg = f"⚠️ DENIED: Track ID #{track_id} violation/non-PPE ({class_name.upper()})"
                        if msg not in event_logs:
                            event_logs.insert(0, msg)
                            log_records.append({"Track ID": track_id, "Detection": class_name.upper(), "Access Status": "DENIED"})

            if not active_objects_in_frame:
                metric_gate.metric("Gate Status", "CLOSED 🔴")
                gate_banner.info("🔒 Gate Status: CLOSED (No Person Detected)")
            elif has_active_violation or not has_active_ppe:
                metric_gate.metric("Gate Status", "DENIED ❌")
                gate_banner.error("⛔ ACCESS DENIED! PPE Kit Missing or Safety Violation Detected!")
                if enable_siren:
                    winsound.Beep(1200, 150)
            else:
                metric_gate.metric("Gate Status", "ALLOWED 🟢")
                gate_banner.success("✅ ACCESS ALLOWED! All Safety Rules Followed.")

            metric_tracks.metric("Total Unique Tracks", len(unique_tracks))
            metric_compliant.metric("Compliant Count", len(compliant_tracks - violation_tracks))
            metric_violations.metric("Violations Detected", len(violation_tracks))

            log_text = "\n".join(event_logs[:12]) if event_logs else ("✅ Monitoring Active: Safety PPE Verified." if has_active_ppe else "⚠️ DENIED: No PPE Detected")
            log_area.code(log_text, language="text")

            if log_records:
                table_placeholder.dataframe(pd.DataFrame(log_records), use_container_width=True)

            annotated_frame = results[0].plot()
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            st_frame.image(annotated_frame, channels="RGB", use_container_width=True)

        cap.release()