
import cv2
import time, numpy as np
import HandTrackingModule as htm
import pyautogui

from Cam import Cam
from Zoom import Zoom
from Scroll import Scroll
from Volume import Volume
from Cursor import Cursor
from OcrKeyboard import OcrKeyboard

detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

mode = ''
active = 0
zoom = False
pTime = 0

pyautogui.FAILSAFE = False

obj_zoom = Zoom()
obj_scroll = Scroll()
obj_volume = Volume()
obj_cursor = Cursor()
obj_ocrKeyboard = OcrKeyboard()
obj_Cam = Cam()


while True:
    
    success, orign_img, wCam, hCam = obj_Cam.runCam()

    orign_img=cv2.flip(orign_img,1)
    orign_img = detector.findHands(orign_img, draw=False)
    orign_lmList = detector.findPosition(orign_img, draw=False)

    orign_fingers = detector.fingersUp()  # 손가락 올라감(1), 내려감(0)

    lmList = orign_lmList
    fingers = orign_fingers
    img = orign_img


    if len(orign_lmList) != 0:    # fingers[] 체크

        if (orign_fingers == [0,0,0,0,0]) & (active == 0 ):   # 주먹
            mode='N'
        elif (orign_fingers[1:] == [1, 1, 1, 1] ) & (active == 0 ):   # 손바닥
            mode = 'Zoom'
            zoom = True
            active, mode, cx1, cx2, cy1, cy2 = obj_zoom.initZoom(fingers, lmList, wCam, hCam)

################## Zoom 👇👇👇👇###################그
    if mode == 'Zoom':

        if fingers == [0, 0, 0, 0, 0]: 
            active = 0
            mode = 'N'

    if zoom == True:
        img, lmList, fingers = obj_zoom.runZoom(img, lmList, fingers, cx1, cx2, cy1, cy2)

        # 확대된 이미지에서 모드 선택
        if (fingers == [0,0,0,0,0]) & (active == 0 ):   # 주먹
            mode='N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) & (active == 0 ):   # 검지
            mode = 'Scroll'
            active = 1
        elif (fingers == [1, 1, 0, 0, 0] ) & (active == 0 ):    # 엄지, 검지
             mode = 'Volume'
             active = 1
        elif (fingers == [1, 1, 1, 0, 0] ) & (active == 0 ):   # 손바닥
             mode = 'Cursor'
             active = 1
        elif (fingers == [1, 0, 0, 0, 1] ) & (active == 0 ):   # 손바닥
             mode = 'Keyboard'
             active = 1



    if mode == 'Scroll':
        active = 1
        img , active, mode = obj_scroll.runScroll(img, lmList, fingers)
        putText(mode)

    if mode == 'Volume':
        active = 1
        img , active, mode = obj_volume.runVolume(img, lmList, fingers)
        putText(mode)


    if mode == 'Cursor':
        active = 1
        img , active, mode = obj_cursor.runCursor(img, lmList, fingers)
        putText(mode)

    if mode == 'Keyboard':
        active = 1
        img , active , mode = obj_ocrKeyboard.runOcrKeyboard(img, lmList, fingers)
        cv2.setWindowProperty('Hand LiveFeed', cv2.WND_PROP_TOPMOST, 1)
        putText(mode)
            

    cTime = time.time()
    fps = 1/((cTime + 0.01)-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(480,50), cv2.FONT_ITALIC,1,(255,0,0),2)

    cv2.imshow('Hand LiveFeed', img)
    cv2.setWindowProperty('Hand LiveFeed', cv2.WND_PROP_TOPMOST, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




    def putText(mode,loc = (250, 450), color = (0, 255, 255)):
        cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_TRIPLEX,
                    3, color, 3)