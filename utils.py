import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp
from pathlib import Path
# pyrefly: ignore [missing-import]
from mediapipe.tasks.python.vision import drawing_utils
import time
import os

# init " pTime = time.time() " before the While loop
def get_fps(cap, pTime,type='default'):
    if type == "default":
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        return fps, pTime

    elif type =="cap":
        fps= cap.get(cv2.CAP_PROP_FPS)
        if fps<= 0:
            return 30, pTime
        return fps, pTime
    else:
        return 30, pTime


def get_macos_volume():
    """Gets current system volume (0 to 100)"""
    try:
        val = os.popen("osascript -e 'output volume of (get volume settings)'").read().strip()
        return int(val) if val.isdigit() else 0
    except Exception:
        return 0


def set_macos_volume(volume_level):
    """Sets system volume (0 to 100)"""
    # Clamp the volume level between 0 and 100
    volume_level = max(0, min(100, int(volume_level)))
    os.system(f"osascript -e 'set volume output volume {volume_level}'")

def HUD(img, vol ,cx, cy, radius = 45, thickness = 6):

        # Generates a color shifting smoothly from Green (low vol) to Blue (high vol)
        hud_color = (0, int(255 - (vol * 2.55)), int(vol * 2.55))
        # 1. Draw a subtle background track ring
        cv2.circle(img, (cx, cy), radius, (80, 80, 80), 2)
        # 2. Draw the active volume arc filling clockwise (starting from the top at -90 degrees)
        end_angle = -90 + int(vol * 3.6)
        cv2.ellipse(img, (cx, cy), (radius, radius), 0, -90, end_angle, hud_color, thickness)
        # 3. Print the percentage text centered inside the ring
        cv2.putText(img, f"{vol}%", (cx - 20, cy + 7), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)