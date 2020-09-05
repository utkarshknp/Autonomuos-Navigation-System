import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial
import time



ser = serial.Serial("COM11")
print(ser.name)
# while True:
# 	ser.write(b"right;")
# 	#time.sleep(0.5)
# ser.close()
# cap = cv2.VideoCapture('track.mp4')
cap = cv2.VideoCapture(1)
count = 0
while(True):
	_, img = cap.read()
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	blur_or = cv2.GaussianBlur(gray,(51,51),0)
	height = gray.shape[0]
	width = gray.shape[1]
	vertices = [(0, 0),(0, height / 4),( width , height / 4),(width, 0)]
	cv2.fillPoly(gray, np.int32([vertices]), 0)


	blur = cv2.GaussianBlur(gray,(51,51),0)
	final = (blur.T - 0.95 * np.average(blur_or,axis = 1).T).T
	# print (final)
	final = np.absolute(-final + np.absolute(final)) / 2
	# change array into uint8 ( float 64 not suppoted by findContours)
	final = cv2.convertScaleAbs(final)
	# change threshold to small value in case of error
	_,threshold = cv2.threshold(final,np.average(final),255,cv2.THRESH_BINARY) 

	# change array into uint8 ( float 64 not suppoted by findContours)
	threshold = cv2.convertScaleAbs(threshold)
	# print (height/4)
	hist = np.sum(threshold[ int(height/ 4) : height ][:], axis=0)
	max2 = np.max(hist[int(width/2):width])
	max1 = np.max(hist[0:(int(width/2)+1)])


	A = 0
	sum_0 = 0
	sum_1 = 0
	peakth = 10000
	if(max1>4500):
	    for j in range (int(width/2)):
	        if(hist[j]>(peakth)):
	            sum_0=sum_0+1
	if(max2>4500):
	    for j in range (int(width/2)):
	        if(hist[j+int(width/2)-1]>(peakth)):
	            sum_1=sum_1+1

	if count == 0:
		time.sleep(4)
		count = 1

	if((sum_0-sum_1) > 80):
		# angle = right_angle
		print ('right')
		ser.write(b"80,")
	elif((sum_1-sum_0) > 80) :
		# angle = left_angle
		print ('left')
		ser.write(b"57,")		
	else:
		# angle = zero_angle
		print ('straight')
		ser.write(b"68,")


	cv2.imshow('a',img)
	cv2.imshow('c',threshold)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
ser.close()
cv2.destroyAllWindows()

