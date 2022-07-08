import cv2
from vpython import *
import getLandmarks

scene.background = vector(0,0,0)

get = getLandmarks.landmarks()
#sequence in which bone ends should be connected
poseLinks = [(10,3),(3,0),(3,1),(1,4),(4,6),(3,2),(2,5),(5,7),(10,8),(8,11),(11,13),(13,15),(10,9),(9,12),(12,14),(14,16)]

poseBones = []
for i in range(16): #total 16 nodes in modified skeleton
    bone = get.bone()
    poseBones.append(bone)

# cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture('./test videos/video by antoni shkraba 1(pexels.com).mp4')
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    _, frame = cam.read()
    if _:
        myPose = get.pose(frame)
        if myPose != []:
            for i,links in enumerate(poseLinks):
                fromPos = vector(myPose[links[0]][0],-myPose[links[0]][1],-myPose[links[0]][2])
                toPos = vector(myPose[links[1]][0],-myPose[links[1]][1],-myPose[links[1]][2])
                poseBones[i].pos = fromPos
                ax = toPos-fromPos
                poseBones[i].axis = ax
                length = sqrt(ax.x*ax.x + ax.y*ax.y + ax.z*ax.z)
                poseBones[i].size = vector(length,length*0.2,length*0.2)

        cv2.imshow('camera',frame)
    if cv2.waitKey(1) & 0xff == ord('q'): # to quit the camera press 'q'
        print('end')
        break
cam.release()
cv2.destroyAllWindows()