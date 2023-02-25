import cv2
import pyautogui


class Scroll:

    def __init__(self):
        pass

    def runScroll(self, img, lmList, fingers):
        active = 1
        
        if len(lmList) != 0:

            global mode
            mode = 'Scroll'

            if fingers == [0,1,0,0,0]:  # 검지 up 위로 스크롤

                cv2.putText(img, 'U', (200,455), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (51, 102, 255), 3)
                pyautogui.scroll(300)

            if fingers == [0,1,1,0,0]:  # V 모양 아래로 스크롤
 
                cv2.putText(img, 'D', (200,455), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (153, 0, 51), 3)
                pyautogui.scroll(-300)
            
            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'

        return img, active, mode

