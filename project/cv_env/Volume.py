import cv2
import math
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class Volume:
    
    devices = AudioUtilities.GetSpeakers()
    
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()   #(-63.5, 0.0, 0.5) min max

    minVol = volRange[0]
    maxVol = volRange[1]

    hmin = 50
    hmax = 200

    volBar = 400
    volPer = 0
    vol = 0

    color = (0,215,255)

    def __init__(self):
        pass
    
    def runVolume(self, img, lmList, fingers):

        active = 1
        
        if len(lmList) != 0:

            if fingers[-1] == 1:
                active = 0
                global mode
                mode = 'N'
        

            else:
                mode = 'Volume'
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 10, self.color, cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, self.color, cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), self.color, 3)
                cv2.circle(img, (cx, cy), 8, self.color, cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)
                length = 2 * length


                vol = np.interp(length, [50, 300], [self.minVol, self.maxVol])
                volBar = np.interp(length, [50, 300], [400, 150])
                volPer = np.interp(length, [50, 300], [0, 100])
    
                self.volume.SetMasterVolumeLevel(vol, None)

                if length < 100:
                    cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)

                cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
                cv2.rectangle(img, (30, int(volBar)), (55, 400), (215, 255, 127), cv2.FILLED)
                cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)
        
        return img, active, mode
