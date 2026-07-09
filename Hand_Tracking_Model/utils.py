# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp
from pathlib import Path
# pyrefly: ignore [missing-import]
from mediapipe.tasks.python.vision import drawing_utils
import time

# custom styles
custom_dots = drawing_utils.DrawingSpec(color=(255, 0, 0),
                                        thickness=5, 
                                        circle_radius=4
                                        )

custom_lines = drawing_utils.DrawingSpec(color=(0, 255, 0), 
                                        thickness=5
                                        )

class handDetector():

    def __init__(self, 
                model_path='hand_landmarker.task', 
                num_hands = 4,
                confidence = 0.5 ) :
        
        # Arguments
        self.model_path = model_path
        self.num_hands = num_hands
        self.confidence = confidence
        # APIs
        self.baseOptions = mp.tasks.BaseOptions
        self.handLandmarker = mp.tasks.vision.HandLandmarker
        self.handLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        # Options configuration
        self.options = self.handLandmarkerOptions(
            base_options=self.baseOptions(model_asset_path=self.model_path),
            running_mode=self.VisionRunningMode.VIDEO,  
            num_hands=self.num_hands,
            min_hand_detection_confidence=self.confidence
        )
        # Build 
        self.landmarker = self.handLandmarker.create_from_options(self.options)

    def findHands(self,img,res, draw=True, draw_finger=-1, coor_finger=-1):

        all_hands = []
        if res.hand_landmarks:
            for hand in res.hand_landmarks:

                if draw :
                    drawing_utils.draw_landmarks(
                        img,
                        hand,
                        mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS,
                        landmark_drawing_spec=custom_dots,
                        connection_drawing_spec=custom_lines,
                        )

                lmList = []
                for id , lm in enumerate(hand):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w) , int(lm.y*h)
                    lmList.append([id,cx,cy])

                all_hands.append(lmList)
        
        if draw_finger != -1 :
            for hand in all_hands :

                if len(all_hands) != 0:
                    cx , cy = hand[draw_finger][1],hand[draw_finger][2]
                    img = cv2.circle(img, (cx,cy),25,(201,97,48),cv2.FILLED)
        
        if coor_finger != -1 :
            i=1
            fingerList = []

            for hand in all_hands :
                if len(all_hands) != 0:
                    cx , cy = hand[coor_finger][1],hand[coor_finger][2]
                    fingerList.append(['Hand '+str(i),cx,cy])
                    i += 1
            return fingerList
        
        return all_hands

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
