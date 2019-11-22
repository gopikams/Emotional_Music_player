import cv2
import numpy as np
import argparse
import time
import glob
import os
import pandas
from win32com.client import Dispatch
from keras.models import load_model
from statistics import mode
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
from time import sleep
from os import listdir 
from os.path import isfile , join 
from tkinter import *
from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk
import sys


count = 1 # Multiple frames intake for accuracy
exitloop=0
flag=1 # Trigger the first loop
USE_WEBCAM = True # If false, loads video file source

# parameters for loading data and images
emotion_model_path = './models/emotion_model.hdf5'
emotion_labels = get_labels('fer2013')
emotion_text="demo"
sog=1


# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
emotion_classifier = load_model(emotion_model_path)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

# starting video streaming
video_capture = cv2.VideoCapture(0)

# Select video or webcam feed
cap = None
if (USE_WEBCAM == True):
    cap = cv2.VideoCapture(0) # Webcam source
else:
    cap = cv2.VideoCapture('./demo/dinner.mp4') # Video file source

while cap.isOpened(): # True:
    ret, bgr_image = cap.read()

    #bgr_image = video_capture.read()[1]

    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    
    count += 1
    if (count % 10==0 ):

        for face_coordinates in faces:
        
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue
        
            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
            print ("Emotion is ", emotion_text)
            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_text, color, 0, -45, 1, 1)
    if(emotion_text=='neutral' or emotion_text == 'angry' or emotion_text == 'sad' or emotion_text == 'happy' or emotion_text == 'surprise' or emotion_text == 'fear' ):   
        #print("Exiting emotion detection")
        break        

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

class MyFirstGUI:

    count =1
    sog=1     
    puse=1   



    def __init__(self, master):

        mp = Dispatch("WMPlayer.OCX")
        path="C:/Users/HP/Documents/audiopro/"+emotion_text+"/"+str(self.sog)+".mp3"
        print(path)
            
        tune = mp.newMedia(path)
        print(emotion_text+" song is playing.")
        mp.currentPlaylist.appendItem(tune)
                

        def playsong():

            if (self.count!=0):
                #print("Running")
                        
                mypath = "C:/Users/HP/Documents/audiopro/"+emotion_text+"/"
                        
                mp.controls.play()
                sleep(1)
                mp.controls.playItem(tune)
                

                event_happened = False
                while not event_happened:
                    event = pygame.event.wait()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #do_something()
                        event_happened = True

        
        def stopsong():
            mp.controls.stop()
            self.sog=1
            

        def pauseresume():
            if(self.puse==1):
            
                mp.controls.pause()                
                self.puse=0
            
            else:
            
                mp.controls.play()
                self.puse=1
            

        def nextsong():
            self.count+=1
            self.sog=self.sog%5
            self.sog+=1

            if (self.count!=0):
                path="C:/Users/HP/Documents/audiopro/"+emotion_text+"/"+str(self.sog)+".mp3"
                print(path)
            
                tune = mp.newMedia(path)
                print(emotion_text+" song is playing.")
                mp.currentPlaylist.appendItem(tune)
                
                mp.controls.play()
                sleep(1)
                mp.controls.playItem(tune)
                   

                event_happened = False
                while not event_happened:
                    event = pygame.event.wait()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #do_something()
                        event_happened = True
                

        
        self.master = master
        master.title("Emotional Music Player")

        Label(root, text="The song played from playlist ").pack(side=LEFT, padx=5, pady=10)
        e = StringVar()
        Entry(root, width=20, textvariable=e).pack(side=TOP)
        e.set(emotion_text)
        

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()
        self.close_button.place(x=180,y=400)

        self.button1 = Button(master, text="Play",command=playsong)
        self.button1.pack()
        self.button1.place(x=180,y=200)
        
        
        self.button4 = Button(master, text="Pause/Resume",command=pauseresume)
        self.button4.pack()   
        self.button4.place(x=180,y=250)   

        self.button2 = Button(master, text="Next",command=nextsong)
        self.button2.pack()
        self.button2.place(x=180,y=300)      
            
        self.button3 = Button(master, text="Stop",command=stopsong)
        self.button3.pack() 
        self.button3.place(x=180,y=350)      
    
      

root = Tk()

C = Canvas(root, bg="blue", height=550, width=500)
filename = PhotoImage(file = "C:\\Users\\HP\\Documents\\Emotion-mastertk\\pic.png")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()  

my_gui = MyFirstGUI(root)
root.mainloop()
