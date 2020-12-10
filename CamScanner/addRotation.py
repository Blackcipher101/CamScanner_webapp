import cv2
import numpy as np

def addRotation(image,degree):
  (h,w)=image.shape[:2]
  (cx,cy)=(w//2,h//2)

  matrix=cv2.getRotationMatrix2D((cx,cy),degree,1.0)
  required=cv2.warpAffine(image,matrix,(w,h))
  return required