# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
#import time

class circle_data:
	data = 'color, min_max, pix_number, cumulative_x, cumulative_y \
	center_mass, correspondence, orientation'
	
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
		self._orientation = 0

def assignment(colour,minx, miny, maxx, maxy, pix_number, center_of_mass):
	colour._minx = minx
	colour._miny = miny
	colour._maxx = maxx
	colour._maxy = maxy
	colour._pix_number = pix_number
	colour._center_mass = center_of_mass
	#colour._cumulative_x = cumulative_x
	#colour._cumulative_y = cumulative_y
	#colour._center_mass = [cumulative_x/pix_number, cumulative_y/pix_number]
	return colour
		
def limits(a,b,minx, miny, maxx, maxy):
	if minx == 0 and miny == 0 and \
	maxx == 0 and maxy == 0:
		minx, maxx = a, a
		miny, maxy = b, b
	else:
		if a < minx:
			minx = a
		elif a > maxx:
			maxx = a
		if b < miny:
			miny = b
		elif b > maxy:
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
	
def print_box(image, data, box_color):
	for z in range(4):
		if z == 0:
			for y in range(data._miny, data._maxy):
				image[data._minx,y] = box_color#(0,255,0)
		if z == 1:
			for y in range(data._miny, data._maxy):
				image[data._maxx,y] = box_color#(0,255,0)
		if z == 2:
			for y in range(data._minx, data._maxx):
				image[y,data._miny] = box_color#(0,255,0)	
		else:
			for y in range(data._minx, data._maxx):
				image[y,data._maxy] = box_color#(0,255,0)
	return image

def DFS(image, labels2, x2, y2, count):
	stack = [[x2,y2]]
	count += 1
	remaining = 0
	first_time = 0
	count_aux = 0
	pix_num, cumul_x, cumul_y = 0, 0, 0
	minix, miniy, maxix, maxiy = 0, 0, 0, 0
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

def DFS2(image, labels2, x2, y2, count):
	stack = [[x2,y2]]
	count += 1
	remaining = 0
	first_time = 0
	count_aux = 0
	pix_num, cumul_x, cumul_y = 0, 0, 0
	minix, miniy, maxix, maxiy = 0, 0, 0, 0
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
		pix_num += 1
		cumul_x += c
		cumul_y += d
		if minix == 0 and miniy == 0 and \
		maxix == 0 and maxiy == 0:
			minix, maxix = c, c
			miniy, maxiy = d, d
		else:
			if c < minix:
				minix = c
			elif c > maxix:
				maxix = c
			if d < miniy:
				miniy = d
			elif d > maxiy:
				maxiy = d
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
	return labels2, count, pix_num, [cumul_x, cumul_y], [minix, miniy, maxix, maxiy]

def euclidean_dist(xy_vals1, xy_vals2):
	#print xy_vals1, xy_vals2
	xval = abs(xy_vals1[0] - xy_vals2[0])
	yval = abs(xy_vals1[1] - xy_vals2[1])
	xpow = pow(xval, 2)
	ypow = pow(yval, 2)
	magnitude = math.sqrt(xpow + ypow)
	return magnitude
	
def reducing_color(color_struct):
	max = 0
	color_len = len(color_struct)
	if color_len > 1:
		for x in range(color_len):
			if color_struct[color_len - x - 1][0] < 320 or \
			color_struct[color_len - x - 1][0] > 520:
				#print x
				color_struct.pop(color_len - x - 1)
			if x == color_len - 1 and len(color_struct) > 1:
				for y in range(len(color_struct)):
					if color_struct[len(color_struct) - x - 1][0] > max:
						max = color_struct[len(color_struct) - x - 1][0]
				for y in range(len(color_struct)):
					if color_struct[len(color_struct) - x - 1][0] != max:
						color_struct.pop(len(color_struct) - x - 1)
	return color_struct
	
def reducing_yellow(color_struct):
	max = 0
	color_len = len(color_struct)
	if color_len > 3:
		for x in range(color_len):
			if color_struct[color_len - x - 1][0] < 320 or \
			color_struct[color_len - x - 1][0] > 520:
				#print x
				color_struct.pop(color_len - x - 1)
			'''
			if x == color_len - 1 and len(color_struct) > 1:
				for y in range(len(color_struct)):
					if color_struct[len(color_struct) - x - 1][0] > max:
						max = color_struct[len(color_struct) - x - 1][0]
				for y in range(len(color_struct)):
					if color_struct[len(color_struct) - x - 1][0] != max:
						color_struct.pop(len(color_struct) - x - 1)
			'''
	return color_struct
	
# Main function
if __name__ == "__main__":
	e1 = cv2.getTickCount()
	
	#cap = cv2.VideoCapture(0)
	
	#while(True):
	#ret, img = cap.read()
	#if(ret):
	# Number of robots
	bot_num = 3
	
	# Colors structure
	colors = []
	for x in range(bot_num):
		colors.append(circle_data())
	
	# Open image manually
	img_name = 'pic17.png'
	img = cv2.imread(img_name)
	width, height,depth = img.shape
	#print width, height

	# HSV image
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Create a black image, a window
	#hsv = np.zeros((width,height,3), np.uint8)
	#opening = np.zeros((width,height*4,3), np.uint8)
	#cv2.namedWindow('hsv')
	#cv2.namedWindow('max')
	#erode_mask = img2  

	# Colors
	##red_low = np.array([0, 113, 64])
	##red_up = np.array([13, 214, 142])
	#red_low = np.array([0, 140, 80])
	#red_up = np.array([179, 170, 122])
	red_low2 = np.array([0, 42, 0])
	red_up2 = np.array([12, 255, 182])
	red_low3 = np.array([155, 42, 0])
	red_up3 = np.array([179, 255, 182])

	#green_low = np.array([68, 67, 25])
	#green_up = np.array([100, 255, 100])
	green_low = np.array([60, 100, 0])
	green_up = np.array([96, 255, 91])

	blue_low = np.array([104, 78, 0])
	blue_up = np.array([130, 255, 124])

	yellow_low = np.array([21, 50, 65])
	yellow_up = np.array([36, 255, 122])
	
	#color_global_low = np.array([21, 0, 0])
	#color_global_up = np.array([179, 255, 126])
	color_global_low = np.array([0, 124, 0])
	color_global_up = np.array([179, 255, 129])

	# Threshold the HSV image
	#red = cv2.inRange(hsv, red_low, red_up)
	red = np.zeros((height,width,3), np.uint8)
	red2 = cv2.inRange(hsv, red_low2, red_up2)
	red3 = cv2.inRange(hsv, red_low3, red_up3)
	red = cv2.bitwise_or(red2, red3, red)
	green = cv2.inRange(hsv, green_low, green_up)
	blue = cv2.inRange(hsv, blue_low, blue_up)
	yellow = cv2.inRange(hsv, yellow_low, yellow_up)
	#color_global = cv2.inRange(hsv, color_global_low, color_global_up)
	
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
	red_opening2 = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel)
	green_opening2 = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
	blue_opening2 = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
	yellow_opening2 = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel)
	#color_glb_opening2 = cv2.morphologyEx(color_global, cv2.MORPH_OPEN, kernel)
	
	red_opening = cv2.dilate(red_opening2, kernel, iterations=1)
	green_opening = cv2.dilate(green_opening2, kernel, iterations=1)
	blue_opening = cv2.dilate(blue_opening2, kernel, iterations=1)
	yellow_opening = cv2.dilate(yellow_opening2, kernel, iterations=1)
	#color_glb_opening = cv2.dilate(color_glb_opening2, kernel, iterations=2)
	# Images mixed
	color_glb2 = np.zeros((height,width,3), np.uint8)
	color_glb3 = np.zeros((height,width,3), np.uint8)
	color_glb = np.zeros((height,width,3), np.uint8)
	color_glb2 = cv2.bitwise_or(red_opening, green_opening, color_glb2)
	color_glb3 = cv2.bitwise_or(color_glb2, blue_opening, color_glb3)
	color_glb_opening = cv2.bitwise_or(color_glb3, yellow_opening, color_glb)
	
	#width2, height2 = red_opening.shape
	#print width2, height2
	
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
	cv2.imshow('global open', color_glb_opening)
	cv2.waitKey(0)
	'''
	
	# Getting max and min relative values for further image processing

	rel_minx, rel_miny, rel_maxx, rel_maxy = 0, 0, 0, 0
	for y in range(height):
		row = color_glb_opening[:,y]
		#print row
		max_row = max(row)
		if max_row > 0:
			if rel_maxy == 0 and rel_miny == 0:
				#rel_maxx, rel_minx = x, x
				rel_maxy, rel_miny = y, y
			else:
				if y > rel_maxy:
					rel_maxy = y
					
	for x in range(width):
		col = color_glb_opening[x,:]
		max_col = max(col)
		if max_col > 0:
			if rel_maxx == 0 and rel_minx == 0:
				rel_maxx, rel_minx = x, x
				#rel_maxy, rel_miny = y, y
			else:
				if x > rel_maxx:
					rel_maxx = x
	
	#print rel_maxx, rel_maxy, rel_minx, rel_miny
	
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
	red_counter, green_counter, blue_counter = 0, 0, 0
	red_colors, green_colors, blue_colors = [], [], []
	red_labels = np.zeros((width,height), np.uint8)
	green_labels = np.zeros((width,height), np.uint8)
	blue_labels = np.zeros((width,height), np.uint8)
	cumulatives = 0
	limits = 0
	
	# Getting color data
	for y in range(rel_miny, rel_maxy):
		for x in range(rel_minx, rel_maxx):
			#print width, height
			#print x,y
			'''
			if red_opening[x,y] > 0:
				pixels_red += 1
				cumulative_x_red += x
				cumulative_y_red += y
				minx_red, miny_red, maxx_red, maxy_red = limits(
				x,y,minx_red,miny_red,maxx_red,maxy_red)
			'''
			#DFS(image, labels2, x2, y2, count):
			#return labels2, count, pix_num, cumul_x, cumul_y, 
			#minix, miniy, maxix, maxiy
			
			if red_opening[x,y] > 0 and red_labels[x,y] == 0:
				red_labels, red_counter, pixels, cumulatives, limits = DFS2(red_opening, 
				red_labels, x, y, red_counter)
			
				red_colors.append([pixels, cumulatives[0]/pixels, cumulatives[1]/pixels,
				limits[0], limits[1], limits[2], limits[3]])
				#print 'red', red_colors
			
			'''
			if green_opening[x,y] > 0:
				pixels_green += 1
				cumulative_x_green += x
				cumulative_y_green += y
				minx_green, miny_green, maxx_green, maxy_green = limits(
				x,y,minx_green,miny_green,maxx_green,maxy_green)
			'''
			if green_opening[x,y] > 0 and green_labels[x,y] == 0:
				green_labels, green_counter, pixels, cumulatives, limits = DFS2(green_opening, 
				green_labels, x, y, green_counter)
			
				green_colors.append([pixels, cumulatives[0]/pixels, cumulatives[1]/pixels,
				limits[0], limits[1], limits[2], limits[3]])
				#print 'green', green_colors
			
			'''
			if blue_opening[x,y] > 0:
				pixels_blue += 1
				cumulative_x_blue += x
				cumulative_y_blue += y
				minx_blue, miny_blue, maxx_blue, maxy_blue = limits(
				x,y,minx_blue,miny_blue,maxx_blue,maxy_blue)
			'''
			if blue_opening[x,y] > 0 and blue_labels[x,y] == 0:
				blue_labels, blue_counter, pixels, cumulatives, limits = DFS2(blue_opening, 
				blue_labels, x, y, blue_counter)
			
				blue_colors.append([pixels, cumulatives[0]/pixels, cumulatives[1]/pixels,
				limits[0], limits[1], limits[2], limits[3]])
				#print 'blue', blue_colors
			
	#print pixels_red, pixels_green, pixels_blue
	#print cumulative_x_red, cumulative_x_green, cumulative_x_blue
	#print cumulative_y_red, cumulative_y_green, cumulative_y_blue
	#print (cumulative_x_red / pixels_red, cumulative_y_red / pixels_red)
	#print (cumulative_x_green / pixels_green, cumulative_y_green / pixels_green)
	#print (cumulative_x_blue / pixels_blue, cumulative_y_blue / pixels_blue)
	
	# Popping small or large undesirable objects on each color structure
	# and keeping the biggest one of the remainders
	# Red
	red_colors = reducing_color(red_colors)
	
	# Green
	green_colors = reducing_color(green_colors)
	
	# Blue
	blue_colors = reducing_color(blue_colors)
	
	#print 'red', red_colors
	#print 'green', green_colors
	#print 'blue', blue_colors
	
	
	# Assigning color data to list
	# Red
	minx_red, miny_red, maxx_red, maxy_red = red_colors[0][3],\
	red_colors[0][4], red_colors[0][5], red_colors[0][6]
	pixels_red = red_colors[0][0]
	center = []
	center.append(red_colors[0][1])
	center.append(red_colors[0][2])
	colors[0] = assignment(colors[0], minx_red, miny_red, maxx_red, maxy_red,
	pixels_red, center)
	#print colors[0]._center_mass
	
	# Green
	minx_green, miny_green, maxx_green, maxy_green = green_colors[0][3],\
	green_colors[0][4], green_colors[0][5], green_colors[0][6]
	pixels_green = green_colors[0][0]
	center = []
	center.append(green_colors[0][1])
	center.append(green_colors[0][2])
	colors[1] = assignment(colors[1], minx_green, miny_green, maxx_green, maxy_green,
	pixels_green, center)
	#print colors[1]._center_mass 
	
	# Blue
	minx_blue, miny_blue, maxx_blue, maxy_blue = blue_colors[0][3],\
	blue_colors[0][4], blue_colors[0][5], blue_colors[0][6]
	pixels_blue = blue_colors[0][0]
	center = []
	center.append(blue_colors[0][1])
	center.append(blue_colors[0][2])
	colors[2] = assignment(colors[2], minx_blue, miny_blue, maxx_blue, maxy_blue,
	pixels_blue, center)
	#print colors[2]._center_mass
	
	# Showing centers of mass on a new image and bounding boxes
	img2 = img
	#img2 = cv2.imread(img_name)
	color = (0,255,0)
	for x in range(len(colors)):
		#print colors[x]._minx, colors[x]._miny, colors[x]._maxx, \
		#colors[x]._maxy
		img2[colors[x]._center_mass[0], colors[x]._center_mass[1]] = (0,255,0)
		img2 = print_box(img2,colors[x],color)
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
	yellow_colors2 = []
	#for x in range(bot_num):
	#	yellow_colors2.append(circle_data())
	
	# DFS for yellow color
	yellow_counter = 0
	yellow_labels = np.zeros((width,height), np.uint8)
	#width, height= labels.shape
	#print width, height
	first = 0
	yellow_pixels = 0
	cumulatives_yellow = 0
	limits_yellow = 0
	for y in range(rel_miny, rel_maxy):
		for x in range(rel_minx, rel_maxx):
			if yellow_opening[x,y] > 0 and yellow_labels[x,y] == 0:
				#labels, counter = DFS(yellow_opening, labels, x, y, counter)
				#print yellow_counter
				yellow_labels, yellow_counter, yellow_pixels, \
				cumulatives_yellow, limits_yellow = DFS2(yellow_opening,\
				yellow_labels, x, y, yellow_counter)
				
				yellow_colors2.append([yellow_pixels, 
				cumulatives_yellow[0]/yellow_pixels, cumulatives_yellow[1]/yellow_pixels, 
				limits_yellow[0], limits_yellow[1], limits_yellow[2], 
				limits_yellow[3]])
				#print yellow_colors2
				#return labels2, count, pix_num, [cumul_x, cumul_y], [minix, miniy, maxix, maxiy]
	#np.set_printoptions(threshold='nan')
	#print labels
	
	pixels_1, pixels_2, pixels_3 = 0, 0, 0
	cumulative_x_1, cumulative_x_2, cumulative_x_3 = 0, 0, 0
	cumulative_y_1, cumulative_y_2, cumulative_y_3 = 0, 0, 0
	minx_1, miny_1, maxx_1, maxy_1 = 0, 0, 0, 0
	minx_2, miny_2, maxx_2, maxy_2 = 0, 0, 0, 0
	minx_3, miny_3, maxx_3, maxy_3 = 0, 0, 0, 0
	
	'''
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
	'''
	
	# Getting limits of yellow colors
	for y in range(rel_miny, rel_maxy):
		for x in range(rel_minx, rel_maxx):
			#print y , x
			yellow_colors2 = reducing_yellow(yellow_colors2)
			'''
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
			'''
	#print pixels_1, pixels_2, pixels_3
	
	# Colors structure
	yellow_colors = []
	for x in range(bot_num):
		yellow_colors.append(circle_data())
	
	# Assigning color data to list
	for x in range(len(yellow_colors2)):
		# Yellow 1
		minx_yellow, miny_yellow, maxx_yellow, maxy_yellow = yellow_colors2[x][3],\
		yellow_colors2[x][4], yellow_colors2[x][5], yellow_colors2[x][6]
		pixels_yellow = yellow_colors2[x][0]
		center = []
		center.append(yellow_colors2[x][1])
		center.append(yellow_colors2[x][2])
		yellow_colors[x] = assignment(yellow_colors[x], minx_yellow, \
		miny_yellow, maxx_yellow, maxy_yellow,
		pixels_yellow, center)
		#print yellow_colors[0]._center_mass
	'''
	# Yellow 2
	yellow_colors[1] = assignment(yellow_colors[1], minx_2, miny_2, maxx_2, 
	maxy_2, pixels_2, cumulative_x_2, cumulative_y_2)
	#print yellow_colors[1]._center_mass 
	# Yellow 3
	yellow_colors[2] = assignment(yellow_colors[2], minx_3, miny_3, maxx_3, 
	maxy_3, pixels_3, cumulative_x_3, cumulative_y_3)
	#print yellow_colors[2]._center_mass
	'''
		
	# Showing centers of mass on a new image and bounding boxes
	#img2 = cv2.imread('equ_3.png')
	color = (0,255,255)
	for x in range(len(yellow_colors)):
		#print yellow_colors[x]._minx, yellow_colors[x]._miny, yellow_colors[x]._maxx, \
		#yellow_colors[x]._maxy
		img2[yellow_colors[x]._center_mass[0], yellow_colors[x]._center_mass[1]] = (0,255,255)
		img2 = print_box(img2,yellow_colors[x],color)
	
	#cv2.imshow('center of mass',img2)
	#cv2.waitKey(0)
		
	# Choosing correspondence and calculating orientation
	font = cv2.FONT_HERSHEY_SIMPLEX
	minimum = 0
	#distances = []
	for x in range(len(yellow_colors)):
		distances = []
		xy_vals = []
		for y in range(len(colors)):
			#print x, y
			distance = euclidean_dist(yellow_colors[x]._center_mass, colors[y]._center_mass)
			distances.append(distance)
			x_val = -yellow_colors[x]._center_mass[0] + \
			colors[y]._center_mass[0]
			y_val = -(height - yellow_colors[x]._center_mass[1]) + \
			(height - colors[y]._center_mass[1])
			xy_vals.append([x_val, y_val])
		
		# Orientation in degrees
		minimum = min(distances)
		for z in range(len(distances)):
			if minimum == distances[z]:
				angle_rad = math.atan2(xy_vals[z][1], xy_vals[z][0])
				angle_deg = math.degrees(angle_rad)
				
				if angle_deg >= 0 and angle_deg <= 90:
					angle_deg = 90 - angle_deg
				elif angle_deg > 90 and angle_deg <= 180:
					angle_deg = 360 + (90 - angle_deg)
				else: 
					#angle_deg < 0
					angle_deg = 90 + (-1 * angle_deg)
				
				colors[z]._correspondence = x
				colors[z]._orientation = int(angle_deg)
				(a, b) = colors[z]._center_mass
				# Printing angle as a string on image
				cv2.putText(img2,str(int(angle_deg)),(a,b),font,0.75,
				(255,255,255),1)
			
	
	'''
	# Printing center of mass
	for x in range(len(colors)):
		print colors[x]._orientation
		c = colors[x]._correspondence
		#print c
		print colors[x]._center_mass, yellow_colors[c]._center_mass
	'''
	
	e2 = cv2.getTickCount()
	time = (e2 - e1) / cv2.getTickFrequency()
	print time
	
	cv2.imshow('center of mass',img2)
	cv2.waitKey(0)
	#if cv2.waitKey(1) & 0xFF == ord('q'):
	#	break
		
	#cap.release()
	cv2.destroyAllWindows()