import cv2
import time
import numpy as np
import imutils
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

widthCam, heightCam = 548 , 380 

cap=cv2.VideoCapture(0)
cap.set(3,widthCam)
cap.set(4, heightCam)
pTime =0
volBar = 250
vol = 0
volPer =0


detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success , img = cap.read()
    #img = imutils.resize(img , width = 348 , height=280)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        #print(lmList[4], lmList[4])
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img ,(x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img ,(x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img , (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img ,(cx,cy), 10, (255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1 , y2-y1)

        if length<30:
            cv2.circle(img ,(cx,cy), 10, (0,255,0), cv2.FILLED)

        #hand range 30-300
        #volume range -63.5 - 0.5
        vol = np.interp(length , [30,100], [minVol,maxVol])
        volBar = np.interp(length , [30,100], [250,120])
        volPer = np.interp(length, [30,100],[0,100])
        #print(int(length) ,vol)
        volume.SetMasterVolumeLevel(vol, None)


        cv2.rectangle(img , (35,120), (55,250),(0,225,0),2)
        cv2.rectangle(img , (35,int(volBar)), (55,250),(0,225,0),cv2.FILLED)
        cv2.putText(img , f'{int(volPer)}%', (40,50), cv2.FONT_HERSHEY_PLAIN, 2 , (255,0,0),3)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img , f'FPS:{int(fps)}', (40,350), cv2.FONT_HERSHEY_PLAIN, 2 , (0,0,255),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
