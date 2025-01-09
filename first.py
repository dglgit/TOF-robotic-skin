'''
# This program is to show the histo data from VL53L3CX run on Nucleo.
# Run the ST VL53L3CX Gui first. Select the right sensor ( you can calibrate or not) 
# that connects the optical fibers.( This can also be done with the Realterm) 
# Close the ST VL53L3CX Gui.The Gui will leave either the gui or range channel open.

# Open the Realterm (set up wight with all the good parameters )to check the channels.
# Realterm: Check "Display As" and select Ascii (fifth from the bottom), check "New Line mode" and check "Scrollback" at 200.
# Realterm: Change Baud to 460800, and select serial port Necleo is plug in and highligth "open"
# Realterm: Check +CR in the "Send" menu. Use command "ch_list" and hit "Send ASCII" to see channels openings.
# This program is to show the histo data from VL53L3CX run on Nucleo.
# Run the ST VL53L3CX Gui first. Select the right sensor ( you can calibrate or not) 
# that connects the optical fibers.( This can also be done with the Realterm) 
# Close the ST VL53L3CX Gui.The Gui will leave either the gui or range channel open.

# Open the Realterm (set up wight with all the good parameters )to check the channels.
# Realterm: Check "Display As" and select Ascii (fifth from the bottom), check "New Line mode" and check "Scrollback" at 200.
# Realterm: Change Baud to 460800, and select serial port Necleo is plug in and highligthed "open"
# Realterm: Check +CR in the "Send" menu. Use command "ch_list" and hit "Send ASCII" to see channels openings.
# Realterm: Use the commands such as "ch_close gui" to close the gui channel and "ch_open histo" to open the histo channel. 
# Realterm: Use "ch_list" to check the channel opening again.
# Realterm: Use "enable" to stream data, and use ^C button to stop streaming data
# Realterm: Hit "open" under port to un-highlight and close the port so Python can have access to
# Realterm:the port that you have your Nucleo plugged in, normally shown 1 to 4.
'''
'''
Now this Python program is getting to run and see the Nucleo histo data. Instructions are below.
1. Open a Terminal window on your PC, assuming Python has been installed.
2. Change directory to the program saved in my Documents folder. In this case I enter "cd Documents"
3. Enter "Python First.py" in the terminal to run this program.
4. When the prompt "y" shows up, hit "Enter" a few times until you see the raw histo data showing on the terminal
5. Enter "bar300" to test the histogram graph. The number after bar is the time in seconds.
6. Due to some data mis-transmission reasons, it tends to run shorter time than it is set up.
7. You can continue to run "bar3000" for another longer run after your assigned time is up and "y" prompt shows up.
8. Enter "stop" to stop the program when prompted of "y"
9. You can also close the terminal if want to stop the program.
'''


'''multi line comments can be written here '''


import math 
from serial import Serial as s
import  matplotlib.pyplot as plt
import numpy as np

ser=s('COM4',baudrate=460800,bytesize=8,timeout=2)#opens and initializes the serial port
ser.write(b'enable\r')#tells the board to start sending data

#this function takes a raw string of histo/gui data and index(es) as inputs.
#It turns the raw string to a list of floats and returns the requested 
#index/slice
def get_line(line,idx=None):
	line=str(line)
	nums=line[line.index(':')+1:].split(',')
	if type(idx)==int:
		return float(nums[idx])
	else:
		start,stop=idx
		try:
			return [float(i) for i in nums[start:stop]]
		except:
			print(nums)
			return [-1]

#roi=[40,65]
roi=[40,65]
while True:
	c=input('y: ')#allows user to give live commands to the program
	print(ser.readline())
	if c=='stop':
		break
	elif 'bar' in c:
                #format command as bar<number of iterations>
		try:
			iters=int(c[c.index('r')+1:])
		except:
			iters=200
		count=1
		for i in range(iters):
			line=ser.readline()
			all_nums=get_line(line,[0,-1])
			if all_nums[0]%2==1:
				plt.bar(range(roi[0],roi[1]),get_line(line,roi))
				#plt.bar(range(roi[0],roi[1]),all_nums[roi[0]:roi[1]])
				plt.show(block=False)
				plt.pause(1e-12)
				plt.clf()
                           

ser.close()
exit()
