import cv2
import numpy as np
from PIL import Image
import time

class circle_data:
	data = 'color, min_max, pix_number, cumulative_x, cumulative_y \
	center_mass'
	
	def __init__(self):
		#self.object = 'object %d' %number
		self._color = ()
		self._minx = 0
		self._miny = 0
		self._maxx = 0
		self._maxy = 0
		self._pix_number = 0
		self._cumulative_x = 0
		self._cumulative_y = 0
		self._center_mass = []
		self._correspondence = 0

def assignment(colour,minx, miny, maxx, maxy, pix_number,
cumulative_x,cumulative_y):
	colour._minx = minx
	colour._miny = miny
	colour._maxx = maxx
	colour._maxy = maxy
	colour._pix_number = pix_number
	colour._cumulative_x = cumulative_x
	colour._cumulative_y = cumulative_y
	colour._center_mass = [cumulative_x/pix_number, cumulative_y/pix_number]
	return colour
		
def limits(a,b,minx, miny, maxx, maxy):
	if minx == 0 and miny == 0 and \
	maxx == 0 and maxy == 0:
		minx, maxx = a, a
		miny, maxy = b, b
	else:
		if a < minx:
			minx = a
		if a > maxx:
			maxx = a
		if b < miny:
			miny = b
		if b > maxy:
			maxy = b
	return minx, miny, maxx, maxy
		
def get_center_mass(object):
	averagex, averagey = 0, 0
	cumulative_x = object._cumulative_x
	cumulative_y = object._cumulative_y
	total_pix = object._pix_number
	averagex = cumulative_x / total_pix
	averagey = cumulative_y / total_pix
	return averagex, averagey
	
def print_box(image, data):
	for z in range(4):
		if z == 0:
			for y in range(data._miny, data._maxy):
				image[data._minx,y] = (0,255,0)
		if z == 1:
			for y in range(data._miny, data._maxy):
				image[data._maxx,y] = (0,255,0)
		if z == 2:
			for y in range(data._minx, data._maxx):
				image[y,data._miny] = (0,255,0)	
		else:
			for y in range(data._minx, data._maxx):
				image[y,data._maxy] = (0,255,0)
	return image
	
def DFS(image, labels2, x2, y2, count):
	stack = [[x2,y2]]
	count += 1
	remaining = 0
	first_time = 0
	count_aux = 0
	while len(stack) > 0:
		#dfs = 1
		if first_time == 0:
			c, d = x2, y2
			first_time = 1
		#else:
		#	c, d = c_aux, d_aux
		
		#while dfs == 1 and len(stack) > 0:
		labels2[c, d] = count
		count_aux += 1
		#print count
		# Analysing remaining neighbors
		for b in range(-1, 2):
			for a in range(-1, 2):
				if  c + a >= 0 and \
					c + a <= width - 1 and \
					d + b >= 0 and \
					d + b <= height - 1 and \
					labels2[c + a, d + b] == 0 and \
					image[c + a, d + b] > 0:
						#print 'DOUBLE FOR'
						remaining += 1
						c_aux, d_aux = c + a, d + b
						a_aux, b_aux = a, b
						#print remaining
						#print c_aux, d_aux
						#if c_aux == 14 and d_aux == 45:
						#	print image[c_aux, d_aux], labels[c_aux, d_aux]
	
		if remaining > 1:
			#print 'APPEND'
			stack.append([c + a_aux,d + b_aux])
			c, d = c_aux, d_aux
		elif remaining == 1:
			#print 'TAKE'
			c, d = c_aux, d_aux
		else:
			#print 'POP'
			c, d = stack.pop()
		remaining = 0
		
		#if count_aux <= 20:
		#		count += -1
		#print remaining
		#counter += 1
		#print stack
	#else:
	#	break
	return labels2, count

# Main function
if __name__ == "__main__":
	# Number of robots
	bot_num = 3
	
	# Colors structure
	colors = []
	for x in range(bot_num):
		colors.append(circle_data())
	
	# Open image
	img = cv2.imread('equ_3.png')
	width, height,depth = img.shape
	print width, height

	# HSV image
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Create a black image, a window
	#hsv = np.zeros((width,height,3), np.uint8)
	#opening = np.zeros((width,height*4,3), np.uint8)
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
	
	'''
	# Showing hsv binary images
	cv2.imshow('red',red)
	cv2.waitKey(0)
	cv2.imshow('green',green)
	cv2.waitKey(0)
	cv2.imshow('blue',blue)
	cv2.waitKey(0)
	cv2.imshow('yellow',yellow)
	cv2.waitKey(0)
	'''
	
	# Opening (Erode then dilate)
	kernel = np.ones((5,5),np.uint8)
	#erode_img = cv2.erode(img,kernel,iterations=2)
	red_opening = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel)
	green_opening = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
	blue_opening = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
	yellow_opening = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel)
	
	#red_opening = cv2.dilate(red_opening2, kernel, iterations=2)
	#green_opening = cv2.dilate(green_opening2, kernel, iterations=2)
	#blue_opening = cv2.dilate(blue_opening2, kernel, iterations=2)
	
	width2, height2 = red_opening.shape
	print width2, height2
	
	'''
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
	'''
	
	pixels_red, pixels_green, pixels_blue = 0, 0, 0
	cumulative_x_red, cumulative_x_green, cumulative_x_blue = 0, 0, 0
	cumulative_y_red, cumulative_y_green, cumulative_y_blue = 0, 0, 0
	minx_red, miny_red, maxx_red, maxy_red = 0, 0, 0, 0
	minx_green, miny_green, maxx_green, maxy_green = 0, 0, 0, 0
	minx_blue, miny_blue, maxx_blue, maxy_blue = 0, 0, 0, 0
	
	'''
	e1 = cv2.getTickCount()
	e2 = cv2.getTickCount()
	time = (e2 - e1) / cv2.getTickFrequency()
	print time
	'''
	
	# Getting color data
	for y in range(height):
		for x in range(width):
			#print width, height
			#print x,y
			if red_opening[x,y] > 0:
				pixels_red += 1
				cumulative_x_red += x
				cumulative_y_red += y
				minx_red, miny_red, maxx_red, maxy_red = limits(
				x,y,minx_red,miny_red,maxx_red,maxy_red)
			
			if green_opening[x,y] > 0:
				pixels_green += 1
				cumulative_x_green += x
				cumulative_y_green += y
				minx_green, miny_green, maxx_green, maxy_green = limits(
				x,y,minx_green,miny_green,maxx_green,maxy_green)
			
			if blue_opening[x,y] > 0:
				pixels_blue += 1
				cumulative_x_blue += x
				cumulative_y_blue += y
				minx_blue, miny_blue, maxx_blue, maxy_blue = limits(
				x,y,minx_blue,miny_blue,maxx_blue,maxy_blue)
				
	#print pixels_red, pixels_green, pixels_blue
	#print cumulative_x_red, cumulative_x_green, cumulative_x_blue
	#print cumulative_y_red, cumulative_y_green, cumulative_y_blue
	#print (cumulative_x_red / pixels_red, cumulative_y_red / pixels_red)
	#print (cumulative_x_green / pixels_green, cumulative_y_green / pixels_green)
	#print (cumulative_x_blue / pixels_blue, cumulative_y_blue / pixels_blue)
	
	# Assigning color data to list
	# Red
	colors[0] = assignment(colors[0], minx_red, miny_red, maxx_red, maxy_red,
	pixels_red, cumulative_x_red, cumulative_y_red)
	#print colors[0]._center_mass
	# Green
	colors[1] = assignment(colors[1], minx_green, miny_green, maxx_green, 
	maxy_green, pixels_green, cumulative_x_green, cumulative_y_green)
	#print colors[1]._center_mass 
	# Blue
	colors[2] = assignment(colors[2], minx_blue, miny_blue, maxx_blue, 
	maxy_blue, pixels_blue, cumulative_x_blue, cumulative_y_blue)
	#print colors[2]._center_mass
	
	# Showing centers of mass on a new image and bounding boxes
	img2 = cv2.imread('equ_3.png')
	for x in range(len(colors)):
		#print colors[x]._minx, colors[x]._miny, colors[x]._maxx, \
		#colors[x]._maxy
		img2[colors[x]._center_mass[0], colors[x]._center_mass[1]] = (0,255,0)
		img2 = print_box(img2,colors[x])
		'''
		# Can save 0.0002 seconds
		for z in range(4):
			if z == 0:
				for y in range(colors[x]._miny, colors[x]._maxy):
					img2[colors[x]._minx,y] = (0,255,0)
			if z == 1:
				for y in range(colors[x]._miny, colors[x]._maxy):
					img2[colors[x]._maxx,y] = (0,255,0)
			if z == 2:
				for y in range(colors[x]._minx, colors[x]._maxx):
					img2[y,colors[x]._miny] = (0,255,0)	
			else:
				for y in range(colors[x]._minx, colors[x]._maxx):
					img2[y,colors[x]._maxy] = (0,255,0)
		'''

	#cv2.imshow('center of mass',img2)
	#cv2.waitKey(0)
	
	# Yellow color structure
	yellow_colors = []
	for x in range(bot_num):
		yellow_colors.append(circle_data())
	
	# DFS for yellow color
	counter = 0
	labels = np.zeros((width,height), np.uint8)
	#width, height= labels.shape
	#print width, height
	first = 0
	for y in range(height):
		for x in range(width):
			if yellow_opening[x,y] > 0 and labels[x,y] == 0:
				labels, counter = DFS(yellow_opening, labels, x, y, counter)
	
	#np.set_printoptions(threshold='nan')
	#print labels
	
	pixels_1, pixels_2, pixels_3 = 0, 0, 0
	cumulative_x_1, cumulative_x_2, cumulative_x_3 = 0, 0, 0
	cumulative_y_1, cumulative_y_2, cumulative_y_3 = 0, 0, 0
	minx_1, miny_1, maxx_1, maxy_1 = 0, 0, 0, 0
	minx_2, miny_2, maxx_2, maxy_2 = 0, 0, 0, 0
	minx_3, miny_3, maxx_3, maxy_3 = 0, 0, 0, 0
	
	
	test = Image.new('L', (height, width), "black")
	test_pix = test.load()
	print width, height
	
	for y in range(height):
		for x in range(width):
			if labels[x,y] > 0:
				test_pix[x,y] = labels[x,y] * 20
	test.show()
	
	test = [0]
	for y in range(height):
		for x in range(width):
			if labels[x,y] > 0:
				for z in range(len(test)):
					if labels[x,y] == test[z]:
						break
					if z == len(test) - 1 and labels[x,y] != test[z]:
						test.append(labels[x,y])
	print test
	
	# Getting 
	for y in range(height):
		for x in range(width):
			#print y , x
			if labels[x,y] == 1:
				pixels_1 += 1
				cumulative_x_1 += x
				cumulative_y_1 += y
				minx_1, miny_1, maxx_1, maxy_1 = limits(
				x,y,minx_1,miny_1,maxx_1,maxy_1)
			
			if labels[x,y] == 2:
				pixels_2 += 1
				cumulative_x_2 += x
				cumulative_y_2 += y
				minx_2, miny_2, maxx_2, maxy_2 = limits(
				x,y,minx_2,miny_2,maxx_2,maxy_2)
			
			if labels[x,y] == 3:
				pixels_3 += 1
				cumulative_x_3 += x
				cumulative_y_3 += y
				minx_3, miny_3, maxx_3, maxy_3 = limits(
				x,y,minx_3,miny_3,maxx_3,maxy_3)
	
	print pixels_1, pixels_2, pixels_3
	
	# Assigning color data to list
	# Yellow 1
	yellow_colors[0] = assignment(yellow_colors[0], minx_1, miny_1, maxx_1, maxy_1,
	pixels_1, cumulative_x_1, cumulative_y_1)
	print yellow_colors[0]._center_mass
	# Yellow 2
	yellow_colors[1] = assignment(yellow_colors[1], minx_2, miny_2, maxx_2, 
	maxy_2, pixels_2, cumulative_x_2, cumulative_y_2)
	print yellow_colors[1]._center_mass 
	# Yellow 3
	yellow_colors[2] = assignment(yellow_colors[2], minx_3, miny_3, maxx_3, 
	maxy_3, pixels_3, cumulative_x_3, cumulative_y_3)
	print yellow_colors[2]._center_mass
	
	# Showing centers of mass on a new image and bounding boxes
	img2 = cv2.imread('equ_3.png')
	for x in range(len(yellow_colors)):
		#print yellow_colors[x]._minx, yellow_colors[x]._miny, yellow_colors[x]._maxx, \
		#yellow_colors[x]._maxy
		img2[yellow_colors[x]._center_mass[0], yellow_colors[x]._center_mass[1]] = (0,255,0)
		img2 = print_box(img2,yellow_colors[x])
	
	cv2.imshow('center of mass',img2)
	cv2.waitKey(0)
	
	cv2.destroyAllWindows()
	