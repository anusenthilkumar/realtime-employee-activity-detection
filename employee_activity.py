import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import mediapipe as mp
import time
import numpy as np
import smtplib
import threading
import schedule
from email.mime.text import MIMEText
from datetime import datetime

# ------------------ EMAIL CONFIG ------------------
EMAIL = "anuastra05@gmail.com"
PASSWORD = "yksq tfyr bjqf ntxo"   # ⚠️ NO SPACES
HR_EMAIL = "anusenthilkumar13@gmail.com"

# ------------------ MEDIAPIPE SETUP ------------------
mp_face_detection = mp.solutions.face_detection
mp_pose = mp.solutions.pose

face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
pose = mp_pose.Pose()

# ------------------ VARIABLES ------------------
inactive_timestamps = []
last_movement_time = time.time()
prev_nose_position = None

inactive_threshold_eyes = 3
inactive_threshold_body = 5

# ------------------ EMAIL FUNCTION ------------------
def send_daily_summary():
    print("📧 Attempting to send email...")

    today_date = datetime.now().strftime("%Y-%m-%d")

    if not inactive_timestamps:
        body = f"Employee was active all day on {today_date}. ✅"
    else:
        body = f"Inactivity Report ({today_date}):\n\n"
        for ts in inactive_timestamps:
            body += f"- {ts.strftime('%H:%M:%S')}\n"

    msg = MIMEText(body)
    msg["Subject"] = "Employee Activity Report"
    msg["From"] = EMAIL
    msg["To"] = HR_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email failed:", e)

# ------------------ SCHEDULER ------------------
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 🔥 TEST MODE (every 1 min)
schedule.every(1).minutes.do(send_daily_summary)

threading.Thread(target=run_scheduler, daemon=True).start()

# 🔥 Send one email immediately
send_daily_summary()

# ------------------ CAMERA ------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not working")
    exit()

# ------------------ MAIN LOOP ------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera error")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_results = face_detection.process(frame_rgb)
    pose_results = pose.process(frame_rgb)

    status = "Active"
    eyes_closed = False

    # -------- FACE DETECTION --------
    if face_results.detections:
        for detection in face_results.detections:
            bbox = detection.location_data.relative_bounding_box
            h = int(bbox.height * frame.shape[0])

            # Simple approximation (not real eye detection)
            if h < frame.shape[0] * 0.1:
                eyes_closed = True

    # -------- BODY MOVEMENT --------
    if pose_results.pose_landmarks:
        nose = pose_results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.NOSE
        ]
        current_position = (nose.x, nose.y)

        if prev_nose_position:
            movement = np.linalg.norm(
                np.array(current_position) - np.array(prev_nose_position)
            )
            if movement > 0.01:
                last_movement_time = time.time()

        prev_nose_position = current_position

    # -------- STATUS LOGIC --------
    current_time = time.time()

    if eyes_closed and (current_time - last_movement_time) > inactive_threshold_eyes:
        status = "Sleeping 😴"
    elif (current_time - last_movement_time) > inactive_threshold_body:
        status = "No Movement ⚠️"

    # -------- STORE INACTIVITY --------
    if "Sleeping" in status or "No Movement" in status:
        now = datetime.now()

        if not inactive_timestamps or (now - inactive_timestamps[-1]).seconds > 60:
            inactive_timestamps.append(now)
            print(f"⚠️ Inactive at {now.strftime('%H:%M:%S')}")

    # -------- DISPLAY --------
    color = (0, 255, 0)
    if "Sleeping" in status or "No Movement" in status:
        color = (0, 0, 255)

    cv2.putText(frame, f"Status: {status}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Employee Activity Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ------------------ CLEANUP ------------------
cap.release()
cv2.destroyAllWindows()