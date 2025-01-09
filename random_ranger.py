import random
import time
stepservo0 = [0,2,4,6,8]
stepservo1= [9,12,15,18,21]
stepservo2=[10,13,16,19,22]

i=0
for i in range(5): #sequential angles feed to servo0
   
    print(" sequential number from servo0 is: ", stepservo0[i])
    time.sleep(2)
    print("zero item from servo0 is: ", stepservo0[0])
    time.sleep(2)

for i in range(5): #sequential angles feed to servo1
   
    print(" sequential number from servo1 is: ", stepservo1[i])
    time.sleep(2)
    print("zero item from servo1 is: ", stepservo1[0])
    time.sleep(2)

for i in range(5): #sequential angles feed to servo2
   
    print("sequential item from servo2 is: ", random.choice(stepservo2))
    time.sleep(2)
    print("zero item from servo2 is: ", stepservo2[0])
    time.sleep(2)

for i in range(5): #random angles feed to servo2
   
    print(" random number from servo0 is: ", stepservo0[i])
    time.sleep(2)
    print("zero item from servo0 is: ", stepservo0[0])
    time.sleep(2)

for i in range(5):#random angles feed to servo1
   
    print("random item from servo1 is: ", random.choice(stepservo1))
    time.sleep(2)
    print("zero item from servo1 is: ", stepservo1[0])
    time.sleep(2)
    
for i in range(5):#random angles feed to servo2
   
    print("random item from servo2 is: ", random.choice(stepservo2))
    time.sleep(2)
    print("zero item from servo2 is: ", stepservo2[0])
    time.sleep(2)

for i in range(5):#random angles feed to servo0, servo1 and servo2
   
    print("random item from servo0 is: ", random.choice(stepservo0))
    print("random item from servo1 is: ", random.choice(stepservo1))
    print("random item from servo2 is: ", random.choice(stepservo2))
   
    print("zero item from servo0, servo1, servo2 are: ", random.choice(stepservo0),random.choice(stepservo1), stepservo2[0])
    time.sleep(2)
    
