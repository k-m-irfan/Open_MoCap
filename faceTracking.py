import cv2
from vpython import *
import getLandmarks

scene.background = color.white

getFace = getLandmarks.mpFace()

facePoints = []
for f in range(478):
    ball = sphere(pos=vector(0,0,0),radius=.005,color=vector(0,1,0))
    facePoints.append(ball)

cam = cv2.VideoCapture(0)
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    _, frame = cam.read()
    if _:
        myFace = getFace.landMarks(frame)
        if myFace != []:
            for indx,lm in enumerate(myFace):
                pos = vector(lm[0],-lm[1],-lm[2])
                facePoints[indx].pos = pos
    # cv2.imshow('camera',frame)
    if cv2.waitKey(1) & 0xff == ord('q'): # to quit the camera press 'q'
        print('end')
        break
cam.release()
cv2.destroyAllWindows()