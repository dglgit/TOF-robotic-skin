#This program serves two purposes:
#1. to take training data by enter a "filename" after first prompt
#2. to validte the effctive by compairing the current
#   data with the training data used by importing the
#   dict_mappint.py program which should include the training data
#3.This program can be run, after hitting many enters, by
#  entering 'bar4000000' or any number after bar
#4. The Python program Ser_test.py was run to set up the Nucleo borad
#5. color_mask.py includes the center and the color filtering of the apple 
#6. cv_plot.py is to show the bar diagram on the cornor
import cv2
import math 
from serial import Serial as s
import  matplotlib.pyplot as plt
import numpy as np
import time
from color_mask import *
from cv_plot import *
from dict_mapping import *
ser=s("/dev/ttyACM0",baudrate=460800,bytesize=8,timeout=1)#opens com4 on the front next to mouse and initializes the serial port
ser.write(b'enable\r')#tells the board to start sending data
cap=cv2.VideoCapture(0)


def suspend():
    ser.write(b'disable\r')
    while 1:
        try:
            get_line(ser.readline())
        except:
            return

#class to write to another file
class write:
    def __init__(self,fname):
        self.fname=fname
        self.stuff=[]
    def w(self, line):
        if self.fname!='':
            self.stuff.append(line)
            with open(self.fname,'a') as df:
                strlist=[float(i) for i in line]
                df.write(str(strlist)[1:-1]+'\n')
    def finish(self):
        if self.fname!='':
            with open(self.fname,'a') as df:
                for i in self.stuff:
                    strlist=[str(num) for num in i]
                    df.write(''.join(strlist)+'\r\n')
    def wipe(self):
        if self.fname!='':
            with open(self.fname,'w') as df:
                df.write('')
#to_write=write('histo_mapping_val.txt')
to_write=write(input('Trainning file name to write to: '))
to_write.wipe()
#this function takes a raw string of histo/gui data and index(es) as
#inputs. It turns the raw string to a list of floats and returns the requested 
#index/slice
def ele_mul(l,x):
    new=[]
    for i,j in enumerate(l):
        new.append(j*(x**i))
    return sum(new)
def apply_coe(j):
    #k0,k1,k2,k3=[2.855,0.00031724,-6.6835e-009,5.2138e-014]
    #k10,k11,k12,k13=[2.7971,0.00039001,-6.5714e-009,4.5944e-014]
    #k20,k21,k22,k23=[1.3994,0.0020301,-1.5862e-007,4.1808e-012]    
    # not for any fit k0,k1,k2,k3=[0,1,0,0]
    ks=np.array([[0,0.00031724,-6.6835e-009,5.2138e-014],
    [0,0.00039001,-6.5714e-009,4.5944e-014],
    [0,0.0020301,-1.5862e-007,4.1808e-012]])
    return [ele_mul(ks[i],j[i]) for i in range(len(ks))]
    
def get_line(line,idx):
    line=str(line)
    nums=line[line.index(':')+1:].split(',')
    if type(idx)==int:
        return float(nums[idx])
    else:
        start,stop=idx
        try:
            return np.array([float(i) for i in nums[start:stop]])
        except:
            print(line)
            return [-1]
def stop():
    ser.write(b'disable\r')
    while 1:
        try:
            get_line(ser.readline())
        except:
            return
roi=[40,60] #put the indices of the slice here
list_roi=np.array([22,24,29]) #22,24 and 29 are the channels
#cap=cv2.videoCapture(0)

while True:
    c=input('y: ')                         #allows user to give live commands to the program
    print(ser.readline())
    if c=='stop':
        break
    elif 'bar' in c:
                                       #format command as bar<number of iterations>(no space)
        try:
            iters=int(c[c.index('r')+1:])
        except:
            iters=200
        count=1
        been=[]
        for i in range(iters):
            line1=ser.readline()                  #requests a line from the serial to read
            all_nums1=get_line(line1,[0,-1])      #turns the serial line to numbers
            if all_nums1[0]%2==1:
                line1=ser.readline()
                all_nums1=get_line(line1,[0,-1])
            #time.sleep(1e-12)                     #gives the serial time to get another line to yield
            line2=ser.readline()                  #gets another line to read
            all_nums2=get_line(line2,[0,-1])      #turns line into numbers
            '''if (all_nums2[0]-all_nums1[0])!=1:
                time.sleep(1e-12)
                line2=ser.readline()
                all_nums2=get_line(line2,[0,-1])'''
            if len(all_nums1)>1 and len(all_nums2)>1:
                start,stop=roi
                
                all=np.concatenate((all_nums1[start:stop],all_nums2[start:stop]))
                cx,cy=get_img(cap,[(i*50,int(j/320)) for i,j in enumerate(all[list_roi])],tuple(all[list_roi]))
                #map_pred=retrieve(tuple(all[list_roi]),closest)
                #to_write.w(list(all[list_roi])+[cx,cy]+list(map_pred))
                to_write.w(list(all[list_roi])+[cx,cy])
                #to_write.w(all)
                #plt.ylabel("Newton")
                #plt.ylim(0,12)#set y limit
                #print(all[list_roi])
                #print(list(all[list_roi])+[cx,cy],map_pred)
                print(list(all[list_roi])+[cx,cy])
                #plt.bar(range(len(all[list_roi])),apply_coe(all[list_roi])) #all[list_roi]
                '''
                int_bars=(all[list_roi]/350).astype(int)
                bars=bar(int_bars,500)
                cv2.putText(bars,str(list(int_bars)),(50,50),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
                cv2.imshow('bars',bars)
                cv2.waitKey(1)
                '''
                #plt.title(str(apply_coe(all[list_roi])))
                #plt.show(block=False)
                #plt.pause(1e-14)
                #plt.clf()
                
#to_write.finish()
ser.close()
exit()
