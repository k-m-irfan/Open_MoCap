#python version 3.9.7
#opncv-python version = 4.5.4.60
#mediapipe version = 0.8.9.1

class mpFace:
    import mediapipe as mp
    import cv2
    def __init__(self):
        self.faceMesh = self.mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    def landMarks(self,frame):#Full Face Landmarks
        frameRGB = self.cv2.cvtColor(frame,self.cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(frameRGB)
        myFace=[]
        if results.multi_face_landmarks != None:
            for faceLandmarks in results.multi_face_landmarks:
                for lm in faceLandmarks.landmark:
                    myFace.append((lm.x,lm.y,lm.z))         
        return myFace

class mpHands:
    import mediapipe as mp
    import cv2
    def __init__(self,maxHands=2):
        self.findHands=self.mp.solutions.hands.Hands(False,maxHands)
    def landMarks(self,frame):
        myHands=[]
        frameRGB = self.cv2.cvtColor(frame,self.cv2.COLOR_BGR2RGB)
        results = self.findHands.process(frameRGB)
        if results.multi_hand_world_landmarks != None:
            for handLandmarks, type in zip(results.multi_hand_world_landmarks,results.multi_handedness):
                myHand = []
                handLabel = type.classification[0].index
                for lm in handLandmarks.landmark:
                    myHand.append((lm.x,lm.y,lm.z))
                myHands.append(((myHand),handLabel))
        return myHands # [((hand_1),handLabel),((hand_2),handLabel)]

#pose
class mpPose:
    import mediapipe as mp
    import cv2 
    def __init__(self):
        self.pose=self.mp.solutions.pose.Pose()
    def landMarks(self,frame):
        myPose=[]
        frameRGB = self.cv2.cvtColor(frame,self.cv2.COLOR_BGR2RGB)
        results = self.pose.process(frameRGB)
        if results.pose_world_landmarks != None:
            for lm in results.pose_world_landmarks.landmark:
                myPose.append((lm.x,lm.y,lm.z))
        return myPose
