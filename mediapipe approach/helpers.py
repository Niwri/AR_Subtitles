from torch import tensor

def get18Points(image) -> tensor:
  '''
  takes an image, and returns the 18 points untouched
  '''
def normalizePoints(points: tensor) -> tensor:
  '''
  takes the 18 points, and puts all points into this formulae:
  X_i = (X_i - min(X)) /(max(X) - min(X))
  Y_i = (Y_i - min(Y)) /(max(Y) - min(Y))
  '''
  normalizedPoints = tensor()
  # do stuff
  return normalizedPoints

def allDirectoryImageToNormalizedPoints(images) -> tensor:
  '''
  takes a directory of images, and returns a tensor of normalized 18 points
  '''
  allDirectoryNormlalizedPoints = tensor()
  # do stuff
  return allDirectoryNormlalizedPoints

