import cv2
import numpy as np

# Main function
if __name__ == "__main__":
	# Open image
	img = cv2.imread('equ_3.png')
	heigth, width, depth = img.shape

	# HSV image
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Create a black image, a window
	#hsv = np.zeros((width,heigth,3), np.uint8)
	#opening = np.zeros((width,heigth*4,3), np.uint8)
	#cv2.namedWindow('hsv')
	#cv2.namedWindow('max')
	#erode_mask = img2  

	# Colors
	red_low = np.array([130, 0, 18])
	red_up = np.array([179, 255, 191])

	green_low = np.array([68, 67, 25])
	green_up = np.array([100, 255, 100])

	blue_low = np.array([104, 78, 0])
	blue_up = np.array([130, 255, 124])

	yellow_low = np.array([21, 0, 65])
	yellow_up = np.array([72, 150, 147])

	# Threshold the HSV image
	red = cv2.inRange(hsv, red_low, red_up)
	green = cv2.inRange(hsv, green_low, green_up)
	blue = cv2.inRange(hsv, blue_low, blue_up)
	yellow = cv2.inRange(hsv, yellow_low, yellow_up)

	# Showing hsv binary images
	cv2.imshow('red',red)
	cv2.waitKey(0)
	cv2.imshow('green',green)
	cv2.waitKey(0)
	cv2.imshow('blue',blue)
	cv2.waitKey(0)
	cv2.imshow('yellow',yellow)
	cv2.waitKey(0)


	# Opening (Erode then dilate)
	kernel = np.ones((5,5),np.uint8)
	#erode_img = cv2.erode(mask,kernel,iterations=2)
	red_opening = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel)
	green_opening = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
	blue_opening = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
	yellow_opening = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel)

	# Showing opening images
	cv2.imshow('red open',red_opening)
	cv2.waitKey(0)
	cv2.imshow('green open',green_opening)
	cv2.waitKey(0)
	cv2.imshow('blue open',blue_opening)
	cv2.waitKey(0)
	cv2.imshow('yellow open',yellow_opening)
	cv2.waitKey(0)
	#cv2.imshow('image',hsv)
	#cv2.waitKey(0)


	cv2.destroyAllWindows()