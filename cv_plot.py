import cv2
import numpy as np
import time
def bar(data,width=50,height=350, spacing=30):
    back=np.zeros((height+20,len(data)*(width+spacing)))
    count=spacing+width
    for idx,j in enumerate(range(0,back.shape[1],spacing+width)):
        back[0:int(data[idx]),j:count-spacing]=255
        count+=(spacing+width)
    to_show=np.flip(back,axis=0)
    return to_show
if __name__=="__main__":
    for _ in range(100):
        deets=[np.random.randint(1,299) for i in range(10)]
        diagram=bar(deets)
        im=cv2.putText(diagram, str(deets), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
        cv2.imshow('pic',im)
        cv2.waitKey(1)
        time.sleep(0.1)
