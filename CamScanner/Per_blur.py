import cv2
import numpy as np
import string
from . import Sharpen


def per_blur(frame,points):
    pts=[]
    num = string.digits
    print(points)
    x=0
    y=0
    to=""
    for i in range(len(points)-1):
        print(points[i])
        if points[i] in num:
            to=to+points[i]
        if points[i+1]==' ':
            x=int(to)
            to=""
        if points[i+1]==',':
            y=int(to)
            to=""
            pts.append([x,y])

    print(pts)
    img=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image=frame
    su=[]
    for i in range(len(pts)):
        su.append(pts[i][0]+pts[i][1])
    for i in range(len(pts)):
        if min(su)==(pts[i][0]+pts[i][1]):
            pts[i],pts[0]=pts[0],pts[i]
        elif max(su)==(pts[i][0]+pts[i][1]):
            pts[3],pts[i]=pts[i],pts[3]
        elif pts[i][0]>pts[i][1]:
            pts[i],pts[1]=pts[1],pts[i]
        elif pts[i][0]<pts[i][1]:
            pts[i],pts[2]=pts[2],pts[i]
    Gblur = Sharpen.unsharp_mask(img)
    th3 = cv2.adaptiveThreshold(Gblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY,11,6)
    pts1 = np.float32(pts)
    pts2 = np.float32([[0,0],[600,0],[0,700],[600,700]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(th3,M,(600,700))
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    
    return dst
