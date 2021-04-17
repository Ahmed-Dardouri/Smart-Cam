import cv2
import numpy as np
import dlib
import face_recognition
import os
import datetime
import time
import threading
from multiprocessing import Process, Pipe, Event

def CaptureProcess(pipe, read_ev):
    while True:
        video = None
        def read_th():
            success = False
            while True:
                if(success): read_ev.wait()
                while video is None or not video.isOpened(): pass
                success, imageFrame = video.read()
                if(success): 
                    pipe.send(imageFrame)
        r_th = threading.Thread(target=read_th)
        r_th.daemon = True
        r_th.start()
        while True:
            c = (video is None or not video.isOpened())
            if c:
                video = cv2.VideoCapture(0)
            c = (video is None or not video.isOpened())
            if c: 
                time.sleep(0.5)

            elif(not read_ev.is_set()):
                video.grab()

class InferThread(threading.Thread):
    def __init__(self):
        super(InferThread, self).__init__()
        self.daemon = True
    def run(self):
        global cap_read_ev, cap_pipe, encodeListunknown
        while True:
            cap_read_ev.set()
            img = cap_pipe.recv()
            cap_read_ev.clear()
            
            imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame =  face_recognition.face_encodings(imgS,facesCurFrame)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces (encodeListknown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListknown,encodeFace)
                matchIndex = np.argmin(faceDis)
                y1,x2,y2,x1 = faceLoc

                if (matches[matchIndex]):
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    
                elif (faceDis[matchIndex]>0.65):
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    unknownMatches = face_recognition.compare_faces(encodeListunknown,encodeFace)
                    unknownFaceDis = face_recognition.face_distance(encodeListunknown,encodeFace)
                    print(len(unknownFaceDis))
                    if len(unknownFaceDis) > 0:
                        unknownMatchIndex = np.argmin(unknownFaceDis)
                        if not (unknownMatches[unknownMatchIndex]):
                            encodeListunknown.append(encodeFace)
                            cv2.imwrite(path1+'/unknown'+str(datetime.datetime.now())+'.jpg', img[y1:y2,x1:x2])
                    else:
                            encodeListunknown.append(encodeFace)
                            cv2.imwrite(path1+'/unknown'+str(datetime.datetime.now())+'.jpg', img[y1:y2,x1:x2])

                else:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 162, 255), 2)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            win.set_image(img)

win = dlib.image_window()

path='knownFaces'
path1='unknownFaces'
knownFacesImages=[]
knownFaces=[]
KnownList = os.listdir(path)
unknownFacesImages=[]
unknownFaces=[]
unKnownList = os.listdir(path1)


for k in KnownList:
    curImg = cv2.imread(f'{path}/{k}')
    knownFacesImages.append(curImg)
    knownFaces.append(os.path.splitext(k)[0])

for k in unKnownList:
    curImg1 = cv2.imread(f'{path1}/{k}')
    unknownFacesImages.append(curImg1)    
    unknownFaces.append(os.path.splitext(k)[0])

def findencodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if face_recognition.face_encodings(img):
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)  
    return encodeList
encodeListknown = findencodings(knownFacesImages)
encodeListunknown = findencodings(unknownFacesImages)

cap_pipe, cap_child_pip = Pipe()
cap_read_ev = Event()
cap_read_ev.set()

infer_th=InferThread()

cap_process=Process(target=CaptureProcess, args=(cap_child_pip, cap_read_ev))
cap_process.daemon = False
cap_process.start()

infer_th.start()
