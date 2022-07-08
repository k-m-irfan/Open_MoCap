import cv2
from vpython import *
import getLandmarks

scene.background = vector(0,0,0)

get = getLandmarks.landmarks()
#sequence in which bone ends should be connected
handLinks = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(0,9),(9,10),(10,11),(11,12),(0,13),(13,14),(14,15),(15,16),(0,17),(17,18),(18,19),(19,20)]

rightHandBones = []
for i in range(20):
    bone = get.bone()
    rightHandBones.append(bone)

leftHandBones = []
for i in range(20):
    bone = get.bone()
    leftHandBones.append(bone)

cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture('C:/Users/K/Downloads/video by antoni shkraba.mp4')
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    _, frame = cam.read()
    if _:
        myPose=get.pose(frame)
        myHands = get.hands(frame)
        if myHands != [] and myPose!=[]:
            for hand in myHands:
                if hand[1] == 0:
                    # print('right hand')
                    for i,links in enumerate(handLinks):
                        fromPos = vector(-hand[0][links[0]][0],-hand[0][links[0]][1],hand[0][links[0]][2])
                        toPos = vector(-hand[0][links[1]][0],-hand[0][links[1]][1],hand[0][links[1]][2])
                        rightHandBones[i].pos = fromPos+vector(.1,0,0)
                        # rightHandBones[i].pos = fromPos+vector(-myPose[7][0],-myPose[7][1],myPose[7][2])
                        ax = toPos-fromPos
                        rightHandBones[i].axis = ax
                        length = sqrt(ax.x*ax.x + ax.y*ax.y + ax.z*ax.z)
                        rightHandBones[i].size = vector(length,length*0.2,length*0.2)
                        # print(myPose[15],myPose[16],hand[0][0])
                            
                if hand[1] == 1:
                    # print('left hand')
                    for i,links in enumerate(handLinks):
                        fromPos = vector(-hand[0][links[0]][0],-hand[0][links[0]][1],hand[0][links[0]][2])
                        toPos = vector(-hand[0][links[1]][0],-hand[0][links[1]][1],hand[0][links[1]][2])
                        leftHandBones[i].pos = fromPos+vector(-.1,0,0)
                        # leftHandBones[i].pos = fromPos+vector(-myPose[6][0],-myPose[6][1],myPose[6][2])
                        ax = toPos-fromPos # getting axis
                        leftHandBones[i].axis = ax
                        length = sqrt(ax.x*ax.x + ax.y*ax.y + ax.z*ax.z) #getting length
                        leftHandBones[i].size = vector(length,length*0.2,length*0.2)
                    
        # cv2.imshow('camera',frame)
    if cv2.waitKey(1) & 0xff == ord('q'): # to quit the camera press 'q'
        print('end')
        break
cam.release()
cv2.destroyAllWindows()