from torch import tensor
import cv2
import mediapipe as mp
import numpy as np
import torch
  
def normalizePoints(points: tensor) -> tensor:
  '''
  takes the 18 points, and puts all points into this formulae:
  X_i = (X_i - min(X)) /(max(X) - min(X))
  Y_i = (Y_i - min(Y)) /(max(Y) - min(Y))
  '''
  normalizedPoints = points.detach().numpy()
  # do stuff
  maxValues = [np.amax(normalizedPoints[:, 0]), np.amax(normalizedPoints[:, 1]), np.amax(normalizedPoints[:, 2])]
  minValues = [np.amin(normalizedPoints[:, 0]), np.amin(normalizedPoints[:, 1]), np.amin(normalizedPoints[:, 2])]
  rangeValues = [maxValues[i] - minValues[i] for i in range(3)]

  for i in range(3):
    normalizedPoints[:, i] = (normalizedPoints[:, i] - minValues[i]) / rangeValues[i]
  
  normalizedPoints = torch.tensor(normalizedPoints)
  return normalizedPoints

def replaceWithNormal():
  allalphabet=['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']
  for alphabet in allalphabet:
    points = np.load(f"mediapipe approach/landmarkTrainData/{alphabet}.npy").tolist()
    points = [normalizePoints(torch.tensor(point)) for point in points]
    np.save(f"mediapipe approach/landmarkTrainData/{alphabet}.npy", points)


