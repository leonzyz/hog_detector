#!/usr/bin/python

import numpy as np
import cv2
import hog





org=cv2.imread('face.png')
#org=cv2.imread('test.jpeg')
#org=cv2.imread('sq_test.jpg')
#org=cv2.imread('sq_test2.jpg')
hog_detector=hog.hog(6,3)
hog_hist=hog_detector.calc_hog(org)
print org.shape
print hog_hist.shape
hog_pic=hog_detector.HogGray(hog_hist)
hog_pic2=hog_detector.Hogpicture(hog_hist)

cv2.namedWindow('org',cv2.WINDOW_NORMAL)
cv2.namedWindow('hog',cv2.WINDOW_NORMAL)
cv2.namedWindow('hog2',cv2.WINDOW_NORMAL)


cv2.imshow('org',org)
cv2.imshow('hog',hog_pic)
cv2.imshow('hog2',hog_pic2)
while True:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
