# set up Nucleo board to have the seosor #2 and
#histogram graph
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import copy
s=serial.Serial("/dev/ttyACM0",baudrate=460800)
s.write(b'disable\n')
time.sleep(1)
while s.inWaiting()>0:
    print(s.readline(),s.inWaiting())
    print('yeet')
s.write(b'help\r')
time.sleep(0.5)
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())

s.write(b'set_activesensor 2\r')#2 is on the right, #0 is the center one
time.sleep(0.5)
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())

s.write(b'ch_list\r')
time.sleep(0.5)
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())

s.write(b'ch_close range\r')
time.sleep(0.5)
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())
    
s.write(b'ch_list\r')
time.sleep(0.5)
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())
    

s.write(b'ch_open histo\r')
time.sleep(0.5)
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())
    

print('enable')
s.write(b'enable\r')
input('enable: ')
print(s.inWaiting())
while s.inWaiting()>0:
    print(s.readline())
time.sleep(1)
print(s.inWaiting())
print('main')

def ele_mul(l,x):
    new=[]
    for i,j in enumerate(l):
        new.append(j*(x**i))
    return sum(new)
def apply_coe(j):
    ks=np.array([[0,0.00031724,-6.6835e-009,5.2138e-014],
    [0,0.00039001,-6.5714e-009,4.5944e-014],
    [0,0.0020301,-1.5862e-007,4.1808e-012]])
    return [ele_mul(ks[i],j[i]) for i in range(len(ks))]
def to_float(x):
    return [float(i) for i in x]
def getline(lin,idx=(0,-1)):
    line=str(lin)
    try:
        nums=line.split(':')[1].split(',')
    except IndexError:
        print(line.split(':'))
        return
    num_line=np.array(to_float(nums[:-1]))
    if len(idx)==2:
        start,end=idx
        return list(num_line[start:end])
    else:
        return list(num_line[idx])
#main loop
current=getline(s.readline())
for i in range(70000):
    try:
        nums=getline(s.readline())
        #line1=ser.readline() George commented old line before 
        line1=s.readline()
        all_nums1=getline(line1) 
        if all_nums1[0]%2==1:
            #line1=ser.readline() George commented old line before
            line1=s.readline()
            all_nums1=getline(line1,[0,-1]) # one desh between get and line before
        #line2=ser.readline()
        line2=s.readline()
        all_nums2=getline(line2,[0,-1]) # one desh between get and line before
        if nums is not None and current is not None:
            if (nums[0]%2)!=(current[0]%2) and len(current)==len(nums):
                concated=current[40:60]+nums[40:60]
                #print(len(current),len(nums))
                roi=np.array(concated)[np.array([22,24,29])]
                print(roi)
                plt.bar(range(3),roi)
                plt.show(block=False)
                plt.pause(1e-12)
                plt.clf()
        current=copy.copy(nums)
    except KeyboardInterrupt:
        break
s.write(b'disable\n')
time.sleep(1)
while s.inWaiting()>0:
    print(s.readline(),s.inWaiting())
    print('yeet')
s.close()
print('done')
    
