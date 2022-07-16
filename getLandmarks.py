#python version 3.9.7
#opncv-python version = 4.5.4.60
#mediapipe version = 0.8.9.1

from vpython import *
class landmarks():
    import mediapipe as mp
    import cv2  
    def __init__(self):
        self.findHands=self.mp.solutions.hands.Hands(False,2)
        self.findPose=self.mp.solutions.pose.Pose()
        self.faceMesh = self.mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    def hands(self,frame):
        myHands=[]
        frameRGB = self.cv2.cvtColor(frame,self.cv2.COLOR_BGR2RGB)
        results = self.findHands.process(frameRGB)
        if results.multi_hand_world_landmarks != None:
            for handLandmarks, type in zip(results.multi_hand_world_landmarks,results.multi_handedness):
                myHand = []
                handLabel = type.classification[0].index
                bLm = handLandmarks.landmark[0] #hand base landmark coordiante, to shidt origon from centre to wrist
                for lm in handLandmarks.landmark:
                    myHand.append((lm.x-bLm.x,lm.y-bLm.y,lm.z-bLm.z))
                myHands.append(((myHand),handLabel))
        return myHands # [((hand_1),handLabel),((hand_2),handLabel)]
    
    def pose(self,frame):
        myPose=[]
        requiredPoints = [0,11,12,13,14,15,16,23,24,25,26,27,28,31,32]
        frameRGB = self.cv2.cvtColor(frame,self.cv2.COLOR_BGR2RGB)
        results = self.findPose.process(frameRGB)
        if results.pose_world_landmarks != None:
            for i,lm in enumerate(results.pose_world_landmarks.landmark):
                if i in requiredPoints: # collecting required points only
                    if i==11:
                        myPose.append((lm.x,lm.y,lm.z))
                        shoulder1 = vector(lm.x,lm.y,lm.z)
                        continue
                    if i==12:
                        myPose.append((lm.x,lm.y,lm.z))
                        shoulder2 = vector(lm.x,lm.y,lm.z)
                        chestPoint = (shoulder1+shoulder2)/2
                        myPose.append((chestPoint.x,chestPoint.y,chestPoint.z))
                        continue
                    if i==23:
                        myPose.append((lm.x,lm.y,lm.z))
                        hip1 = vector(lm.x,lm.y,lm.z)
                        continue
                    if i==24:
                        myPose.append((lm.x,lm.y,lm.z))
                        hip2 = vector(lm.x,lm.y,lm.z)
                        hipPoint = (hip1+hip2)/2
                        myPose.append((hipPoint.x,hipPoint.y,hipPoint.z))
                        continue
                    myPose.append((lm.x,lm.y,lm.z))
        return myPose

    def face(self,frame):#Full Face Landmarks
        frameRGB = self.cv2.cvtColor(frame,self.cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(frameRGB)
        myFace=[]
        if results.multi_face_landmarks != None:
            for faceLandmarks in results.multi_face_landmarks:
                for lm in faceLandmarks.landmark:
                    myFace.append((lm.x,lm.y,lm.z))         
        return myFace

    def bone(self):
        ball = sphere(pos = vector(0,0,0), radius = 0.005,axis =vector(1,0,0))
        pyramid1 = pyramid(pos = vector(0.02,0,0), size = vector(0.02, 0.02, 0.02), axis = -vector(1,0,0))
        pyramid2 = pyramid(pos = vector(0.02,0,0), size = vector(0.08, 0.02, 0.02),axis = vector(1,0,0))
        Bone = compound([ball,pyramid1,pyramid2],origin=vector(0,0,0),axis = vector(1,0,0))
        return Bone