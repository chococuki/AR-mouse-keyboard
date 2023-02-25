import cv2
import HandTrackingModule as htm
class Zoom :
    
    
    def __init__(self):
        self.detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)
        
    
    def initZoom(self, fingers, lmList, wCam, hCam):
        global cx1, cx2, cy1, cy2
        active = 1
        mode = 'Zoom'
        
        cx0, cy0 = lmList[0][1:]
        cx12, cy12 = lmList[12][1:]
            
        len_x = int(((cx12 - cx0) ** 2 + (cy12 - cy0) ** 2) ** 0.55)
        len_y = int(len_x * 32 / 51)
        len_blank = len_x / 8


        cx, cy = lmList[12][1:]

        cx1 = cx-len_x-4*len_blank
        cy1 = cy-len_y-3*len_blank
        cx2 = cx+len_x+3*len_blank
        cy2 = cy+len_y+4*len_blank


        if cx1 < 0:
            cx2 -= cx1
            cx1 = 0
        if cy1 < 0:
            cy2 -= cy1
            cy1 = 0
        if cx2 > wCam:
            cx1 = cx1 - cx2 + wCam
            cx2 = wCam
        if cy2 > hCam:
            cy1 = cy1 - cy2 + hCam
            cy2 = hCam
            
        return active, mode, cx1, cx2, cy1, cy2

    def runZoom(self,img, lmList, fingers, cx1, cx2, cy1, cy2):

        # 필요한 부분 자르고 확대
        cropped = img[int(cy1):int(cy2), int(cx1):int(cx2)]
        img = cv2.resize(cropped, (640, 480))

        # 확대된 이미지로 다시 손을 찾음
        img = self.detector.findHands(img, draw=True)
        lmList = self.detector.findPosition(img, draw=True)
        fingers = self.detector.fingersUp()
        
        return img, lmList, fingers
    