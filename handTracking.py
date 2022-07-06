import cv2
from vpython import *
import getLandmarks

scene.background = color.white

getHands = getLandmarks.mpHands()

leftHandPoints = []
for lh in range(21): #21 hand landmarks
    ball = sphere(pos=vector(0,0,0),radius=.002,color=vector(0,0,1))
    leftHandPoints.append(ball)

rightHandPoints = []
for rh in range(21):
    ball = sphere(pos=vector(0,0,0),radius=.002,color=vector(1,0,0))
    rightHandPoints.append(ball)

cam = cv2.VideoCapture(0)
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    _, frame = cam.read()
    if _:
        myHands = getHands.landMarks(frame)
        if myHands != []:
            for hand in myHands:
                if hand[1] == 0:
                    # print('right hand')
                    for indx,lm in enumerate(hand[0]):
                        pos = vector(lm[0],-lm[1],-lm[2])+vector(-.1,0,0)
                        rightHandPoints[indx].pos = pos
                if hand[1] == 1:
                    # print('left hand')
                    for indx,lm in enumerate(hand[0]):
                        pos = vector(lm[0],-lm[1],-lm[2])-vector(-.1,0,0)
                        leftHandPoints[indx].pos = pos
    cv2.imshow('camera',frame)
    if cv2.waitKey(1) & 0xff == ord('q'): # to quit the camera press 'q'
        print('end')
        break
cam.release()
cv2.destroyAllWindows()