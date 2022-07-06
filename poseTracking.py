import cv2
from vpython import *
import getLandmarks

scene.background = color.white

getPose = getLandmarks.mpPose()

posePoints = []
for p in range(33):
    ball = sphere(pos=vector(0,0,0),radius=.02,color=vector(0,1,0))
    posePoints.append(ball)

cam = cv2.VideoCapture(0)
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    _, frame = cam.read()
    if _:
        myPose = getPose.landMarks(frame)
        if myPose != []:
            for indx,lm in enumerate(myPose):
                pos = vector(lm[0],-lm[1],-lm[2])
                posePoints[indx].pos = pos
    cv2.imshow('camera',frame)
    if cv2.waitKey(1) & 0xff == ord('q'): # to quit the camera press 'q'
        print('end')
        break
cam.release()
cv2.destroyAllWindows()