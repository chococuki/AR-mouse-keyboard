import cv2

class Cam :
    
    def __init__(self):

        self.wCam, self.hCam = 640, 480
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,self.wCam)
        self.cap.set(4,self.hCam)

    def runCam(self):
        
        success, img = self.cap.read()

        return success, img, self.wCam, self.hCam