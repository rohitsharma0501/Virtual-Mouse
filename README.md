# 🖱️ Virtual Mouse Using Hand Gestures

## 📌 Overview

This project implements a **virtual mouse system** using hand gestures detected through a webcam. It uses computer vision techniques to control the cursor, perform clicks, and take screenshots without physical mouse interaction.

---

## 🚀 Features

* 🖐️ Hand tracking using MediaPipe
* 🎯 Cursor movement using index finger
* 🖱️ Left click gesture
* 🖱️ Right click gesture
* 🖱️ Double click gesture
* 📸 Screenshot capture using gesture
* ⚡ Real-time performance with smooth interaction

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – Video processing
* **MediaPipe** – Hand tracking
* **PyAutoGUI** – Mouse control & screen actions
* **NumPy** – Mathematical calculations
* **Pynput** – Mouse event handling

---

## ⚙️ How It Works

1. Webcam captures live video feed
2. MediaPipe detects hand landmarks
3. Specific finger positions & angles are calculated
4. Gestures are recognized based on:

   * Finger angles
   * Distance between thumb & index finger
5. Corresponding mouse actions are performed
