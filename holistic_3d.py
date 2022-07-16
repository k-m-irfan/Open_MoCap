import cv2
from vpython import *
import getLandmarks

scene.background = vector(0,0,0)

get = getLandmarks.landmarks()
#sequence in which bone ends should be connected
poseLinks = [(10,3),(3,0),(3,1),(1,4),(4,6),(3,2),(2,5),(5,7),(10,8),(8,11),(11,13),(13,15),(10,9),(9,12),(12,14),(14,16)]
handLinks = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(0,9),(9,10),(10,11),(11,12),(0,13),(13,14),(14,15),(15,16),(0,17),(17,18),(18,19),(19,20)]

poseBones = []
for i in range(16): #total 16 nodes in modified skeleton
    bone = get.bone()
    poseBones.append(bone)

rightHandBones = []
for i in range(20):
    bone = get.bone()
    rightHandBones.append(bone)

leftHandBones = []
for i in range(20):
    bone = get.bone()
    leftHandBones.append(bone)

cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture('./test videos/video by antoni shkraba 1(pexels.com).mp4')
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

myHandsOld = [([(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], 0), ([(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], 1)]

while True:
    _, frame = cam.read()
    if _:
        myPose = get.pose(frame)
        myHands = get.hands(frame)
        if myHands == []:
            myHands = myHandsOld
        myHandsOld = myHands

        if myPose != []:
            for i,links in enumerate(poseLinks):
                fromPos = vector(-myPose[links[0]][0],-myPose[links[0]][1],myPose[links[0]][2])
                toPos = vector(-myPose[links[1]][0],-myPose[links[1]][1],myPose[links[1]][2])
                poseBones[i].pos = fromPos
                ax = toPos-fromPos
                poseBones[i].axis = ax
                length = sqrt(ax.x*ax.x + ax.y*ax.y + ax.z*ax.z)
                poseBones[i].size = vector(length,length*0.2,length*0.2)

            lefftHandPosition = vector(-myPose[6][0],-myPose[6][1],myPose[6][2])
            rightHandPosition = vector(-myPose[7][0],-myPose[7][1],myPose[7][2])

            if myHands != []:
                for hand in myHands:
                    if hand[1] == 0:
                        # print('right hand')
                        for i,links in enumerate(handLinks):
                            fromPos = vector(-hand[0][links[0]][0],-hand[0][links[0]][1],hand[0][links[0]][2])+rightHandPosition
                            toPos = vector(-hand[0][links[1]][0],-hand[0][links[1]][1],hand[0][links[1]][2])+rightHandPosition
                            rightHandBones[i].pos = fromPos
                            ax = toPos-fromPos
                            rightHandBones[i].axis = ax
                            length = sqrt(ax.x*ax.x + ax.y*ax.y + ax.z*ax.z)
                            rightHandBones[i].size = vector(length,length*0.2,length*0.2) #length, width and height ration of bone
                                        
                    if hand[1] == 1:
                        # print('left hand')
                        for i,links in enumerate(handLinks):
                            fromPos = vector(-hand[0][links[0]][0],-hand[0][links[0]][1],hand[0][links[0]][2])+lefftHandPosition
                            toPos = vector(-hand[0][links[1]][0],-hand[0][links[1]][1],hand[0][links[1]][2])+lefftHandPosition
                            leftHandBones[i].pos = fromPos
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