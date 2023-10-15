import mediapipe as mp
import cv2
import numpy as np
import os
from datetime import datetime
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

import matplotlib.pyplot as plt # for plotting
import torch.optim as optim #for gradient descent

from helpers import normalizePoints

import serial

torch.manual_seed(1) # set the random seed

class GestureClassifier(nn.Module):
    def __init__(self, name="Model"):
        super(GestureClassifier, self).__init__()
        self.name = name
        self.layer1 = nn.Linear(21*3, 45)
        self.layer2 = nn.Linear(45, 35)
        self.layer3 = nn.Linear(35, 24)
    def forward(self, img):
        flattened = img.view(-1, 21 * 3)
        activation1 = F.relu(self.layer1(flattened))
        activation2 = F.relu(self.layer2(activation1))
        output = self.layer3(activation2)
        return output

def setupNN(PATH: str): 
   model = GestureClassifier()
   model.load_state_dict(torch.load(PATH))
   return model

def predict(model: GestureClassifier, img: np.ndarray) -> str:
   img = normalizePoints(torch.tensor(img))
   img = img.float()
   output = model(img)
   allalphabet = ['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']
   return allalphabet[torch.argmax(output)]

def main(graphicDisplay: bool = True) -> None:
  try:
     ser = serial.Serial('COM3', 9600)
     openSerial = True
  except:
      print("Serial port not opened!")
      openSerial = False
  gestureNN = setupNN("mediapipe approach\model_Sixth_lr0.01_bs_300_epoch2")
  mp_drawing = mp.solutions.drawing_utils
  mp_hands = mp.solutions.hands
  cap = cv2.VideoCapture(1)

  startTime = datetime.now()
  with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands: 
    previousPred = ""
    count = 0
    dedgeTime = datetime.now()
    while cap.isOpened():
      ret, frame = cap.read()
      
      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      # image = cv2.flip(image, 1)
      image.flags.writeable = False
      results = hands.process(image)
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      #actually grabbing the points  
      if results.multi_hand_landmarks:
          dedgeTime = datetime.now()
          handArray = np.empty((0,3), float)
          for hand in results.multi_hand_landmarks:
              for point in mp_hands.HandLandmark:
                  handArray = np.vstack((handArray,[hand.landmark[point].x,hand.landmark[point].y,hand.landmark[point].z]))
              if graphicDisplay:    
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                        )
          # CALL INFERENCE FUNCTION HERE
          prediction = predict(gestureNN, handArray)
          # time.sleep(0.2)
          if previousPred != prediction:
            previousPred = prediction
            flag = False
            startTime = datetime.now()
          elif not flag and (datetime.now() - startTime).total_seconds() > 1:
            flag = True
            count += 1
            print(f"Prediction #{count}:", prediction.upper())
            if openSerial:
                ser.write(prediction.encode())   
      else:  
        if (datetime.now() - dedgeTime).total_seconds() > 2:
            previousPred = ""
            dedgeTime = datetime.now()   

      if graphicDisplay:
        cv2.imshow('Hand Tracking', image)

      if cv2.waitKey(10) & 0xFF == ord('q'):
        break

  cap.release()
  cv2.destroyAllWindows()

main(graphicDisplay=True)