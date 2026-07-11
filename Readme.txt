# ✋ Hands Volume Control 🔊

An interactive, real-time Computer Vision application that lets you control your macOS system volume using hand gestures! Powered by **MediaPipe** and **OpenCV**, this project tracks your hand landmarks via your webcam and dynamically adjusts the volume based on the distance between your thumb and index finger.

---

## ✨ Features

* **🤖 Real-time Hand Tracking**: Powered by MediaPipe's state-of-the-art Hand Landmarker task.
* **🪐 Interactive HUD (Heads-Up Display)**: Displays a beautiful, color-shifting circular volume arc directly on your camera feed (transitioning from green for low volume to blue for high volume).
* **🍎 macOS System Volume Integration**: Uses AppleScript (`osascript`) commands to interactively and smoothly adjust macOS master volume levels (0% to 100%).
* **⚡ Visual Feedback**: Draws connection lines between tracking points that change color based on proximity threshold levels.
* **📈 High Performance**: Includes real-time FPS rendering to monitor system efficiency.

---

## 📂 Project File Structure

Here is how the project files are laid out:

```bash
Hands Volume Control/
├── 📄 main.py                    # 🚀 Main entry point. Handles webcam capture, preprocessing, and the execution loop.
├── 📄 utils.py                   # 🛠️ Helper utilities (FPS counter, HUD renderer, and macOS volume controllers).
├── 📄 requirements.txt           # 📦 Python package dependencies.
└── 📁 Hand_Tracking_Model/       # 🧠 MediaPipe Hand Tracking Module
    ├── 📄 utils.py               # 📐 Defines the handDetector class wrapper for MediaPipe's HandLandmarker.
    └── 💾 hand_landmarker.task   # 🦾 Pre-trained MediaPipe Hand Landmarker model file.
```

---

## 🛠️ Installation & Setup

Follow these simple steps to set up and run the project locally.

### 1. Clone the Repository & Navigate to Project Directory
```bash
cd "Hands Volume Control"
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

> [!NOTE]
> The dependencies include:
> * `mediapipe` (for ML-based hand tracking)
> * `opencv-python` (for webcam capture and drawing)
> * `pycaw` (used in cross-platform/Windows setups, optional here since macOS controls are handled natively)

---

## 🎮 How to Use

To start the application, run:
```bash
python main.py
```

### Gestures:
1. **Calibrate/Track**: Hold your hand up in front of the webcam. Make sure your hand is fully visible.
2. **Adjust Volume**: Bring your **Thumb (landmark 4)** and **Index Finger (landmark 8)** closer or further apart:
   * **Pinch close** (distance < 50 pixels) ➡️ **0% Volume (Muted)** (Line turns **Green** 🟢)
   * **Spread wide** (distance > 300 pixels) ➡️ **100% Volume** (Line turns **Blue** 🔵)
   * **In-between** (distance 50-300 pixels) ➡️ Volume interpolates dynamically (Line is **Red** 🔴)
3. **Exit**: Press the `SPACE` key to stop the camera and close the application windows.

---

## 💻 Tech Stack & API Reference

* **Python 3**
* **OpenCV**: Handles image manipulation, colorspace conversions (BGR to RGB/RGB to BGR), flipping, and rendering the custom circular HUD.
* **MediaPipe Tasks API**: Performs detection in `RunningMode.VIDEO` using the `detect_for_video` method with frame timestamps.
* **AppleScript (`osascript`)**: Directly executes commands to get and set system volume natively.
