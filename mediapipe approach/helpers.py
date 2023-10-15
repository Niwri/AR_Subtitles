from torch import tensor
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def get18Points(image_path: str) -> tensor:
  '''
  takes an image, and returns the 18 points untouched
  '''
  image = cv2.imread(image_path)

  with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands: 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    untouchedtensor = []
    #actually grabbing the points
    if results.multi_hand_landmarks:
        
      for hand in results.multi_hand_landmarks:
        for point in (mp_hands.HandLandmark):
          x = hand.landmark[point].x
          y = hand.landmark[point].y
          z = hand.landmark[point].z
          untouchedtensor.append([x,y,z])
    return tensor(untouchedtensor)                  
                
            
        


  
def normalizePoints(points: tensor) -> tensor:
  '''
  takes the 18 points, and puts all points into this formulae:
  X_i = (X_i - min(X)) /(max(X) - min(X))
  Y_i = (Y_i - min(Y)) /(max(Y) - min(Y))
  '''
  normalizedPoints = tensor()
  # do stuff
  return normalizedPoints

def allDirectoryImageToNormalizedPoints(directory: str) -> tensor:
  '''
  takes a directory of images, and returns a tensor of normalized 18 points
  '''
  allDirectoryNormlalizedPoints = tensor()
  # do stuff
  return allDirectoryNormlalizedPoints

