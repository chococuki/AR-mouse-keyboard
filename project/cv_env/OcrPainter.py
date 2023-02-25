import cv2
import HandTrackingModule as htm
import numpy as np
import os
from keras.models import load_model
import io


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

cap=cv2.VideoCapture(0)
cap.set(3,640)# 넓이
cap.set(4,480) # 높이

detector = htm.handDetector(detectionCon=0.50,maxHands=1)
idx = 0



while True:

    # 1. 카메라 화면 가져오고
    success, img = cap.read() 
    img=cv2.flip(img,1)
    
    # 2. 손 위치 찾기
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList)!=0:

        x1, y1 = lmList[8][1],lmList[8][2]
        x2, y2 = lmList[12][1],lmList[12][2]
        
        # 3. 손가락 갯수 확인
        fingers = detector.fingersUp()

        # 4. 그리기 모드 아님
        if fingers[1] and fingers[2]:            
            xp,yp=0,0
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. 그리기 모드
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1 

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp=x1,y1
           
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50 , 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    key = cv2.waitKey(30)
    if key == ord('r'):
        imgCanvas = np.zeros((480,640,3), np.uint8)
        print("Clear.")
    
    if key == ord('c'):
        
        x_resize = cv2.resize(imgInv, dsize=(32,32), interpolation=cv2.INTER_AREA)
        x_gray = cv2.cvtColor(x_resize, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f'{folderPath}/image_{idx}.png', x_resize)
        imgpath = f'{os.getcwd()}/{folderPath}/image_{idx}.png'
        imgpath = imgpath.replace('\\', '/')
        image = cv2.imread(imgpath)

        #image = 255 - image
        X_data=[]
        X_data.append(image)
        x = np.array(X_data)
        y_prob = model.predict(x)
        y = y_prob.argmax()
        print(y)
        print(label_dict[y])

    if key == ord('q'):
        print("Good bye")
        break


    cv2.imshow("Image", img)
    cv2.waitKey(1)
