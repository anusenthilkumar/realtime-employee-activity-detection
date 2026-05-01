# 🧠 Real-Time Employee Activity Detection

## 📌 Overview

This project focuses on detecting and analyzing employee activity in real time using computer vision techniques. The system uses a webcam to monitor activity and classify employees as **active** or **inactive** based on movement and visual cues.

---

## 🎯 Objective

The main goal of this project is to:

* Monitor employee activity in real time
* Identify inactive states such as sleeping or no movement
* Provide alerts for inactivity
* Improve workplace productivity and monitoring

---

## ⚙️ Technologies Used

* Python
* OpenCV
* YOLO (You Only Look Once)
* MediaPipe (optional for pose/eye detection)
* NumPy

---

## 🧠 Working Principle

1. The webcam captures live video feed
2. Frames are processed using computer vision techniques
3. YOLO detects human presence
4. Movement and eye status are analyzed
5. System classifies activity:

   * Active ✅
   * Inactive ❌
6. Alerts can be generated based on inactivity

---

## 📂 Project Structure

```
RealTime-Employee-Activity-Detection/
│
├── employee_activity.py
├── README.md
└── requirements.txt (optional)
```

---

## ▶️ How to Run

1. Install required libraries:

```
pip install opencv-python numpy mediapipe
```

2. Run the program:

```
python employee_activity.py
```

---

## 🚀 Features

* Real-time detection
* Activity classification
* Lightweight implementation
* Easy to extend with deep learning models

---

## 📊 Applications

* Workplace monitoring
* Smart offices
* Productivity analysis
* Security systems

---

## 🔮 Future Enhancements

* Use CNN model for better accuracy
* Add alert notifications (email/SMS)
* Dashboard for HR monitoring
* Multi-person tracking

---


## ⭐ Conclusion

This project demonstrates how AI and computer vision can be used to monitor employee activity effectively in real-time environments.
