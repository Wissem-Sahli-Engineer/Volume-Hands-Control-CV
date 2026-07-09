import cv2
import time
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import mediapipe as mp

from utils import get_fps

Wcam, Hcam = 1280 , 720 

cap = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)

pTime = time.time()
while True:

    test , img = cap.read()

    if not test or img is None:
        break

    fps , pTime = get_fps(cap, pTime)

    # display 
    cv2.putText(img,f'FPS : {str(int(fps))}',(40,70), cv2.FONT_HERSHEY_COMPLEX,
                3, (183,81,93) , 1
                )
    cv2.imshow('Live',img)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()