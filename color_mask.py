import cv2
import numpy as np
import matplotlib.pyplot as plt
from dict_mapping import *
def get_img(vcap,coords=(),sdata=None):
    ret, frame = vcap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([60,110,80])
    upper_red = np.array([255,255,180])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #mask_blur=cv2.blur(mask,(4,4))
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    M=cv2.moments(cv2.threshold(mask,120,255,0)[1])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
    #cv2.line(res, (20,cX), (20,cY), (255,255,255), 8)
    
    colidx=0
    
    for i in coords:
        col=[0,0,0]
        x,y=i
        col[colidx]=255
        res[-y:,x:x+50]=col #the coordinate of the histogram bar
        #cv2.circle(res,i,5,(255,255,255),-1) draw circle around the bar
        colidx+=1
    if sdata is not None:
        cv2.circle(res,retrieve(tuple(sdata),closest),5,(255,255,0),-1)
    cv2.imshow('res',res)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        return None
    return cX,cY
def distance(x,y):
    #print(x,y,(x[0]-y[0]),(x[1]+y[1]),'pts')
    return ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
def adaptive_img(vcap,coords=(),sensor_data=None,predictor=None,stop=False,npred=(0,0)):
    ret, frame = vcap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([60,110,80])
    upper_red = np.array([255,255,180])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #mask_blur=cv2.blur(mask,(4,4))
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    M=cv2.moments(cv2.threshold(mask,120,255,0)[1])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
    #cv2.line(res, (20,cX), (20,cY), (255,255,255), 8)
    
    colidx=0
    
    for i in coords:
        col=[0,0,0]
        x,y=i
        col[colidx]=255
        res[-y:,x:x+50]=col #the coordinate of the histogram bar
        #cv2.circle(res,i,5,(255,255,255),-1) draw circle around the bar
        colidx+=1
    
    if sensor_data is not None:
        predicted=predictor.predict(sensor_data)
        print(npred,'npred')
        cv2.circle(res,npred,5,(0,255,0),-1)
        if predicted is not None:
            tpredicted=tuple(predicted)
            #print(tpredicted,'tpredict')
            cv2.circle(res,tpredicted,5,(255,255,0),-1)
            loss=distance(tpredicted,(cX,cY))
        else:
            loss=None
            
        if not stop:
            predictor.update((*sensor_data,cX,cY))
        else:
            cv2.circle(res,(0,0),10,(0,0,255),-1)
    cv2.imshow('res',res)
    k = cv2.waitKey(1) & 0xFF
    
    if k == 27:
        return None
    return cX,cY,loss
def get_mean(pts):
    cx=int(pts['m10']/m['m00'])
    cy=int(pts['m01']/m['m00'])
    return cx,cy
#cap=cv2.VideoCapture(0)
def main():
    while 1:
        cx,cy=get_img(cap)
        print(cx,cy)
print(__name__)

#     input('yeet')
    #plt.scatter([cx],[cy])
    #plt.axis([420,220,100,350])
    #plt.show(block=False)
    #plt.pause(1e-12)
    #plt.clf()
