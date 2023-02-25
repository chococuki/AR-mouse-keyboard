import cv2
import numpy as np
import os
import io
import time
import pyautogui
import pyperclip
from keras.models import load_model


class OcrKeyboard():

    path = f'{os.getcwd()}/cv_env/korean.hdf5'
    path = path.replace('\\', '/')
    model = load_model(path)

    lable_file = f'{os.getcwd()}/cv_env/label.txt'
    labels_file = io.open(lable_file, 'r', encoding='utf-8').read().splitlines()
    label_dict = {}
    count = 0
    for label in labels_file:
        label_dict[count] = label
        count += 1

    folderPath="Char"
    
    brushThickness = 25 # 붓 크기
    eraserThickness = 100 # 지우개 크기
    drawColor=(255,0,255) # 색 정하기
    xp, yp = 0, 0

    imgCanvas = np.zeros((480, 640, 3), np.uint8) # 그림 그려질 캠버스 정하기

    def __init__(self):
        pass
    
    def runOcrKeyboard(self, img, lmList, fingers):

        active = 1

        if len(lmList)!=0:
            global mode
            mode = 'Keyboard'

            x1, y1 = lmList[8][1],lmList[8][2]
            x2, y2 = lmList[12][1],lmList[12][2]

            # 4. 그리기 모드 아님
            if fingers[1] and fingers[2]:            
                self.xp,self.yp=0,0
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), self.drawColor, cv2.FILLED)

            # 5. 그리기 모드
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, self.drawColor, cv2.FILLED)

                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = x1, y1 

                cv2.line(img, (self.xp, self.yp), (x1, y1), self.drawColor, self.brushThickness)
                cv2.line(self.imgCanvas, (self.xp, self.yp), (x1, y1), self.drawColor, self.brushThickness)
                self.xp,self.yp=x1,y1
        
            if fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'

            
        imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50 , 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        
        img = cv2.bitwise_and(img,imgInv)
        img = cv2.bitwise_or(img,self.imgCanvas)


        if fingers == [1, 0, 0, 0, 0] :
            self.imgCanvas = np.zeros((480,640,3), np.uint8)
            print("Clear.")
        
        if fingers == [0, 1, 1, 1, 1]:
            
            x_resize = cv2.resize(imgInv, dsize=(32,32), interpolation=cv2.INTER_AREA)
            cv2.imwrite(f'{self.folderPath}/image_0.png', x_resize)
            imgpath = f'{os.getcwd()}/{self.folderPath}/image_0.png'
            imgpath = imgpath.replace('\\', '/')
            image = cv2.imread(imgpath)

            X_data=[]
            X_data.append(image)
            x = np.array(X_data)
            y_prob = self.model.predict(x)
            y = y_prob.argmax()
            print(self.label_dict[y])
            pyperclip.copy(self.label_dict[y])
            pyautogui.hotkey("ctrl","v")
            self.imgCanvas = np.zeros((480,640,3), np.uint8)
            time.sleep(1)
        
        return img, active, mode




    
