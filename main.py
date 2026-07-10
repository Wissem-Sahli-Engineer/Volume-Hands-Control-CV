from math import sqrt
import cv2
import time
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import mediapipe as mp
import math
from utils import get_fps , get_macos_volume , set_macos_volume , HUD
from Hand_Tracking_Model.utils import handDetector


##################
""" Arguments """
##################
Wcam, Hcam = 1280 , 720 

cap = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)

detector = handDetector(model_path = "Hand_Tracking_Model/hand_landmarker.task",
                        num_hands = 1,
                        confidence = 0.6
                        )

frame_count = 0
pTime = time.time()

Alert = "Hand is not completly DETECTED ! Try to move it !"

while True:

    # Reading
    test , img = cap.read()
    if not test or img is None:
        break

    # fps and time
    fps , pTime = get_fps(cap, pTime)

    timestamp_ms = int((frame_count / get_fps(cap,0,type='cap')[0]) * 1000)
    frame_count += 1

    # flipping the image Y-AXIS : 
    img = cv2.flip(img,1)

    # preprocessing

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

    res = detector.landmarker.detect_for_video(mp_img,timestamp_ms) 

    lmList1 = detector.findHands(img,res, draw =True, draw_finger=4  ,coor_finger = 4)[0]
    if len(lmList1) != 0 :
        x1 , y1 = lmList1[1],lmList1[2]

    lmList2 = detector.findHands(img,res, draw =True, draw_finger=8  ,coor_finger = 8)[0]
    if len(lmList2) != 0 :
        x2 , y2 = lmList2[1],lmList2[2]

    if len(lmList1) == 0 or len(lmList2) == 0:

        cv2.putText(img,Alert, (int(Wcam/2)-50,100), cv2.FONT_HERSHEY_COMPLEX,
                    1, (183,81,93) , 1
                    )
        print(Alert)
    else :

        cv2.line(img, (x1,y1) , (x2,y2),
                (0,0,255), 3
                )
        cx , cy = (x1+x2)// 2 , (y1+y2)// 2

        line = int(sqrt((x1-x2)**2 + (y1-y2)**2))
        print(line)

        if line < 50 :
            vol = 0
            cv2.circle( img,(cx,cy),15,
                    (0,255,0),cv2.FILLED )

            cv2.line(img, (x1,y1) , (x2,y2),
                (0,255,0), 3
                )
            set_macos_volume(vol)

        elif line > 300:
            vol = 100
            cv2.circle( img,(cx,cy),15,
                    (255,0,0),cv2.FILLED )

            cv2.line(img, (x1,y1) , (x2,y2),
                (255,0,0), 3
                )
            set_macos_volume(vol)

        else :
            vol = int(np.interp(line, [50, 300], [0, 100]))
            cv2.line(img, (x1,y1) , (x2,y2),
                (0,0,255), 3
                )
            set_macos_volume(vol) 


        """cv2.putText(img,str(vol),(40,360), cv2.FONT_HERSHEY_COMPLEX,
                    3, (183,81,93) , 1
                    )
        """
        

        HUD(img, vol ,cx, cy, radius = 45, thickness = 6)

        print(lmList1,lmList2)


    # display 
    cv2.putText(img,f'FPS : {str(int(fps))}',(40,70), cv2.FONT_HERSHEY_COMPLEX,
                3, (183,81,93) , 1
                )
    cv2.imshow('Live',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()