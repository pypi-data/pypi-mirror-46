from playrobot import Servo
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D

import cv2
import serial
import time

class PiBB:
    def __init__(self):
        self.Speed = 50
        self.visionThread = 100
        self.model = ''
        self.detectPoint =  [(160,40),(200,40),(240,40),(280,40),(319,40)]
        self.colorThread = 150
        
    def dnnInit(self,path):
        model = Sequential()
        model.add(Conv2D(filters=16,kernel_size=(3,3),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(Conv2D(filters=48,kernel_size=(1,1),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Conv2D(filters=24,kernel_size=(3,3),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(Conv2D(filters=24,kernel_size=(3,3),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(2, activation='softmax'))
        model.load_weights(path)

        gray = cv2.imread('bird_binary.jpg',cv2.IMREAD_GRAYSCALE)
        test = cv2.resize(gray,(80,80),interpolation=cv2.INTER_CUBIC).reshape(1, 80, 80, 1).astype('float32')
        test_norm = test/255
        model.predict_classes(test_norm)
        
        self.model = model
        
    def rcCtrl(self,act):
        turn = {1:[self.speed,self.speed],
               2:[self.speed,self.speed],
               3:[self.speed,self.speed],
               4:[self.speed,self.speed]}
        Servo.setServoPulse(0,1500+turn[act][0])
        Servo.setServoPulse(1,1500+turn[act][1])

    def roadTrace(self,img,decide = 0):
        gray = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),self.visionThread,255,cv2.THRESH_BINARY)[1]
        lineState = ''
        for y,x in self.detectPoint:
            lineState += '0' if gray[x][y] == 255 else '1'
            
        for i,j in enumerate(self.detectPoint):
            cv2.putText(img,str(i),j,cv2.FONT_HERSHEY_COMPLEX,1,(0,150,255),1,cv2.LINE_AA)
        
        if lineState == '00000':decide = -1
        elif lineState[:4] == '1111':decide = 2
        elif lineState[1] == '1':decide = 1
        elif lineState[3] == '1':decide = -1
        cv2.putText(img,'right' if decide < 0 else 'left' if decide > 0 else 'front',
                    (50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,150,255),1,cv2.LINE_AA)
        tempColor = self.colorDetect(img)
        if tempColor == 'RED':
            colorToSound = {'RED':'紅色','BLUE':'藍色','GREEN':'綠色'}
            print('偵測到' + colorToSound[tempColor])
            #TTS.wordToSound('偵測到' + colorToSound[COLOR_DEC])
    
        return img,decide

    def autoDrive(self,img):
        decide = 0
        gray = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),self.visionThread,255,cv2.THRESH_BINARY)[1][85:235,80:230]
        cv2.rectangle(img, (85,80), (235, 230), (0, 255, 0), 2)
        showText = ''
    
        test = cv2.resize(gray,(80,80),interpolation=cv2.INTER_CUBIC).reshape(1, 80, 80, 1).astype('float32')
        test_norm = test/255
        self.model.predict_classes(test_norm) == 0
            
        cv2.putText(img,showText,(200,50),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,150,255),1,cv2.LINE_AA)
        
        img,decide = self.roadTrace(img)
        if decide == -1:self.rcCtrl(2)
        elif decide == 1:self.rcCtrl(3)
        elif decide == 2:self.rcCtrl(5)
        else:self.rcCtrl(1)
        return img

    def colorDetect(self,img):
        COLOR =  self.colorThread
        height, width = img.shape[:2]
        height, width = height//2, width//2
        B, G, R = cv2.split(img)
        B, G, R = B[height][width], G[height][width], R[height][width]
        if G > COLOR and B < COLOR and R < COLOR:
            return 'GREEN'
        elif B > COLOR and G < COLOR and R < COLOR:
            return 'BLUE'
        elif R > COLOR and G < COLOR and B < COLOR:
            return 'RED'
        else:
            return 'WHITE'
        
    def run(self):
        self.rcCtrl(1)
        cap = cv2.VideoCapture(0)
        # 設定影像尺寸
        cap.set(3,320)
        cap.set(4,240)
        while True:
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                rgbImage = self.autoDrive(frame)
                cv2.imshow('cam',rgbImage)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    cap.release()
                    self.rcCtrl(8,0)
                    break

class AIoTCar:
    def __init__(self):
        self.Speed = 50
        self.visionThread = 100
        self.model = ''
        self.detectPoint =  [(160,40),(200,40),(240,40),(280,40),(319,40)]
        self.colorThread = 150
        self.ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)
        
    def dnnInit(self,path):
        model = Sequential()
        model.add(Conv2D(filters=16,kernel_size=(3,3),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(Conv2D(filters=48,kernel_size=(1,1),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Conv2D(filters=24,kernel_size=(3,3),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(Conv2D(filters=24,kernel_size=(3,3),padding='same',input_shape=(80,80,1),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(2, activation='softmax'))
        model.load_weights(path)

        gray = cv2.imread('bird_binary.jpg',cv2.IMREAD_GRAYSCALE)
        test = cv2.resize(gray,(80,80),interpolation=cv2.INTER_CUBIC).reshape(1, 80, 80, 1).astype('float32')
        test_norm = test/255
        model.predict_classes(test_norm)
        
        self.model = model
        
    def rcCtrl(self,act):
        self.ser.flush()
        nowCmd = str(act) + '_' + str(self.speed) + '\n'
        self.ser.write(nowCmd.encode())
        
    def roadTrace(self,img,decide = 0):
        global EAT_TIME
        detectPoint = [(160,40),(200,40),(240,40),(280,40),(319,40)]
        gray = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),self.visionThread,255,cv2.THRESH_BINARY)[1]
        lineState = ''
        for y,x in detectPoint:
            lineState += '0' if gray[x][y] == 255 else '1'
            
        for i,j in enumerate(detectPoint):
            cv2.putText(img,str(i),j,cv2.FONT_HERSHEY_COMPLEX,1,(0,150,255),1,cv2.LINE_AA)
        
        if lineState == '00000':decide = -1
        elif lineState[:4] == '1111':decide = 2
        elif lineState[1] == '1':decide = 1
        elif lineState[3] == '1':decide = -1
        cv2.putText(img,'right' if decide < 0 else 'left' if decide > 0 else 'front',
                    (50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,150,255),1,cv2.LINE_AA)
        tempColor = self.colorDetect(img)
        if tempColor == 'RED':
            colorToSound = {'RED':'紅色','BLUE':'藍色','GREEN':'綠色'}
            print('偵測到' + colorToSound[tempColor])
            #TTS.wordToSound('偵測到' + colorToSound[COLOR_DEC])
        return img,decide
    
    def autoDrive(self,img):
        global EAT_TIME,STATE,image
        decide = 0
        gray = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),self.visionThread,255,cv2.THRESH_BINARY)[1][85:235,80:230]
        cv2.rectangle(img, (85,80), (235, 230), (0, 255, 0), 2)
        showText = ''
        if time.time() - EAT_TIME > 30:
            test = cv2.resize(gray,(80,80),interpolation=cv2.INTER_CUBIC).reshape(1, 80, 80, 1).astype('float32')
            test_norm = test/255
            if self.model.predict_classes(test_norm) == 0:
                EAT_TIME = time.time()
                showText = 'food'
                STATE = 'food'
            else:
                showText = 'no food'
        else:
            showText = 'full'
            
        if time.time() - EAT_TIME > 60:
            STATE = 'nofood'
            showText = 'hungary'
            
        cv2.putText(img,showText,(200,50),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,150,255),1,cv2.LINE_AA)
        
        img,decide = self.roadTrace(img)
        if STATE != 'nofood':
            if decide == -1:self.rcCtrl(2,self.speed)
            elif decide == 1:self.rcCtrl(3,self.speed)
            elif decide == 2:
                self.rcCtrl(5,self.speed)
            else:self.rcCtrl(1,self.speed)
        else:
            self.rcCtrl(8,self.speed)
        return img
    
    def colorDetect(self,img):
        COLOR = self.colorThread 
        height, width = img.shape[:2]
        height, width = height//2, width//2
        B, G, R = cv2.split(img)
        B, G, R = B[height][width], G[height][width], R[height][width]
        if G > COLOR and B < COLOR and R < COLOR:
            return 'GREEN'
        elif B > COLOR and G < COLOR and R < COLOR:
            return 'BLUE'
        elif R > COLOR and G < COLOR and B < COLOR:
            return 'RED'
        else:
            return 'WHITE'
        
    def run(self):
        global STATE
        self.rcCtrl(1,self.speed)
        cap = cv2.VideoCapture(0)
        # 設定影像尺寸
        cap.set(3,320)
        cap.set(4,240)
        while True:
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                rgbImage = self.autoDrive(frame)
                cv2.imshow('cam',rgbImage)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    cap.release()
                    self.rcCtrl(8,0)
                    break