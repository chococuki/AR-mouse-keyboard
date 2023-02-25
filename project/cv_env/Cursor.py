import cv2
import pyautogui, autopy
import numpy as np
import time

class Cursor:

    def __init__(self):
        pass
    
    def runCursor(self, img, lmList, fingers):

        active = 1
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

        if fingers[1:] == [0,0,0,0]: #엄지 제외
            active = 0
            global mode
            mode = 'N'

        else:
            mode = 'Cursor'
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                w, h = autopy.screen.size()

                X = int(np.interp(x1, [110, 620], [0, w - 1]))
                Y = int(np.interp(y1, [20, 350], [0, h - 1]))

                cv2.circle(img, (lmList[8][1], lmList[8][2]), 7, (255, 255, 255), cv2.FILLED)
                cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 255, 0), cv2.FILLED)  #thumb


                autopy.mouse.move(X,Y)

                if fingers[0] == 0:
                    cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)  # thumb
                    pyautogui.click()
                    time.sleep(0.2)
                
                if fingers == [1,1,0,0,0]:
                    pyautogui.click(button='right')
                    time.sleep(0.2)
    
        return img, active, mode
