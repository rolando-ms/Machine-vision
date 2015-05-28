#----------------------------------------------------------------------
# "Robot Tracker"
# Author: Rolando Morales 	Date: 17/04/2014
#
# Description: Script with the main purpose of controlling mobile robots
# with a camera. There are also another functionalities to ease this
# main task. The main modules are the following:
#	* robot_detection .- This module does the main task of the script.
#	 					As the name says, it detects a color pattern
#						placed over the robots to return their position
#						and orientation.
#
#	* show_cam .- This module just shows the real-time camera images.
#
#	* thres_adj .- This module helps with the threshold adjustment while
#				showing the real-time result of binarization and after
#				applying the thresholds.
#
#	* show_hsv_binary.- This module shows the binary images of all 
#						colors after binarization.
#
# This script was designed and tested with the following libraries:
#	- Python 2.7.5
#	- OpenCV 2.4.10
#	- Numpy 1.9.0
#	- nxt-python 2.2.2
#	- math (included in python)
#	- Tkinter (included in python)
#----------------------------------------------------------------------
import cv2					# For image preprocessing and printing
import numpy as np			# Requirement for OpenCV
import math					# To calculate data
import time
import nxt.locator			# Tests with NXT
from nxt.motor import *		# Tests with NXT
from Tkinter import *		# To make the GUI
from nxt.motor import Motor, PORT_B, PORT_C	# Distance tests with NXT
from nxt.sensor import Ultrasonic, PORT_4	# Distance tests with NXT
import serial
#import time

# This class includes all the needed data of a detected object.
class circle_data:
	data = 'color, min_max, pix_number, cumulative_x, cumulative_y \
	center_mass, correspondence, orientation'
	
	def __init__(self):
		#self.object = 'object %d' %number
		self._color = ()
		# Coordinates for bounding box
		#-------------
		self._minx = 0
		self._miny = 0
		self._maxx = 0
		self._maxy = 0
		#-------------
		self._pix_number = 0
		self._cumulative_x = 0
		self._cumulative_y = 0
		self._center_mass = []
		self._correspondence = 0
		self._orientation = 0
		
class default:
	def_vals = [0, 42, 0, 12, 255, 182, 155, 42, 0, 179, 255, 182,
	60, 100, 0, 96, 255, 91, 104, 78, 0, 130, 255, 124, 21, 50, 65,
	36, 255, 122]
	
	file_name = 'test.txt'
	
	colors_used = ['red2\n','red3\n','green\n','blue\n','yellow\n']
	
	cam_num = 0

# This module assigns the gathered data to the corresponding variable.
# It is used to make few module calls.
def assignment(colour,minx, miny, maxx, maxy, pix_number, cumulative_x, cumulative_y):
	colour._minx = minx
	colour._miny = miny
	colour._maxx = maxx
	colour._maxy = maxy
	colour._pix_number = pix_number
	#colour._center_mass = center_of_mass
	colour._cumulative_x = cumulative_x
	colour._cumulative_y = cumulative_y
	if cumulative_x == 0 or cumulative_y == 0:
		colour._center_mass = [0, 0]
	else:
		colour._center_mass = [cumulative_x/pix_number, cumulative_y/pix_number]
	return colour		

# The purpose of this module is the same as assignment, but with less
# assignments.
def assignment2(colour,minx, miny, maxx, maxy, pix_number, center_of_mass):
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

# This module takes the actual coordinate values and compares it with
# the max. and min. coordinates.
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

# This module, given the object data, calculates the center of mass with
# the coordinate's mean value.
def get_center_mass(object):
	averagex, averagey = 0, 0
	cumulative_x = object._cumulative_x
	cumulative_y = object._cumulative_y
	total_pix = object._pix_number
	averagex = cumulative_x / total_pix
	averagey = cumulative_y / total_pix
	return averagex, averagey

# This module prints the bounding box of an object and returns an image
# with such box.
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
'''
# This module applies the DFS algorithm to gather all the pixels of an 
# image. It makes the corresponding labelling
def DFS(image, labels2, x2, y2, count):
	width, height = image.shape
	stack = [[x2,y2]] 	# Stack to save pixels
	count += 1			# Label counter
	remaining = 0		# Remaining pixels to count in the neighborhood
	first_time = 0		# Flag of first time run
	count_aux = 0		# auxiliary label counter
	#pix_num, cumul_x, cumul_y = 0, 0, 0
	#minix, miniy, maxix, maxiy = 0, 0, 0, 0
	
	# Run while the stack has pixels with unlabelled neighbors
	while len(stack) > 0:
		# If first run
		if first_time == 0:
			c, d = x2, y2
			first_time = 1

		# Assigning label to pixel
		labels2[c, d] = count
		count_aux += 1
		
		# Analysing remaining neighbors (8 neighbors)
		for b in range(-1, 2):
			for a in range(-1, 2):
				if  c + a >= 0 and \
					c + a <= width - 1 and \
					d + b >= 0 and \
					d + b <= height - 1 and \
					labels2[c + a, d + b] == 0 and \
					image[c + a, d + b] > 0:
						# If true, the remaining counter increases
						remaining += 1
						# Saving pixel coordinates of remaining pixels
						c_aux, d_aux = c + a, d + b
						a_aux, b_aux = a, b
		
		if remaining > 1:
			# Appending pixels with more than 1 remaining neighbors
			stack.append([c + a_aux,d + b_aux])
			c, d = c_aux, d_aux
		elif remaining == 1:
			# Using auxiliary coordinates without saving them
			c, d = c_aux, d_aux
		else:
			# Popping pixel without remaining neighbors
			c, d = stack.pop()
		remaining = 0 # Resetting remaining variable

	return labels2, count
'''
# This module is an extension of the previous DFS module. It also takes
# the number of pixels of a detected object, the cumulative coordinate
# values for the center of mass and the min. and max. coordinate values.
def DFS2(image, labels2, x2, y2, count):
	width, height = image.shape
	stack = [[x2,y2]]
	count += 1
	remaining = 0
	first_time = 0
	count_aux = 0
	pix_num, cumul_x, cumul_y = 0, 0, 0
	minix, miniy, maxix, maxiy = 0, 0, 0, 0
	
	# Run while the stack has pixels with unlabelled neighbors
	while len(stack) > 0:
		# First time run
		if first_time == 0:
			c, d = x2, y2
			first_time = 1
		
		# Assigning label
		labels2[c, d] = count
		count_aux += 1
		pix_num += 1 	# Increasing counter
		cumul_x += c	# Increasing cumulative
		cumul_y += d	# Increasing cumulative
		
		# Getting the max. and min. coordinate values
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
		
		# Analysing remaining neighbors
		for b in range(-1, 2):
			for a in range(-1, 2):
				if  c + a >= 0 and \
					c + a <= width - 1 and \
					d + b >= 0 and \
					d + b <= height - 1 and \
					labels2[c + a, d + b] == 0 and \
					image[c + a, d + b] > 0:
						# If true, the remaining counter increases
						remaining += 1
						# Saving pixel coordinates of remaining pixels
						c_aux, d_aux = c + a, d + b
						a_aux, b_aux = a, b

		if remaining > 1:
			# Appending pixels with more than 1 remaining neighbors
			stack.append([c + a_aux,d + b_aux])
			c, d = c_aux, d_aux
		elif remaining == 1:
			# Using auxiliary coordinates without saving them
			c, d = c_aux, d_aux
		else:
			# Popping pixel without remaining neighbors
			c, d = stack.pop()
		remaining = 0	# Resetting remaining variable

	return labels2, count, pix_num, [cumul_x, cumul_y], [minix, miniy, maxix, maxiy]

# This module calculates the euclidean distance between two given points
def euclidean_dist(xy_vals1, xy_vals2):
	xval = abs(xy_vals1[0] - xy_vals2[0])
	yval = abs(xy_vals1[1] - xy_vals2[1])
	xpow = pow(xval, 2)
	ypow = pow(yval, 2)
	magnitude = math.sqrt(xpow + ypow)
	return magnitude

# This module reduces the color structure when more than 1 object per
# "layer" was detected
def reducing_color(color_struct):
	max = 0
	color_len = len(color_struct)
	if color_len > 1:
		for x in range(color_len):
			try:
				if color_struct[color_len - x - 1][0] < 320 or \
				color_struct[color_len - x - 1][0] > 520:
					# Popping from structure if the object is too small or 
					# too big
					color_struct.pop(color_len - x - 1)
				if x == color_len - 1 and len(color_struct) > 1:
					# Getting max. list value
					for y in range(len(color_struct)):
						if color_struct[len(color_struct) - x - 1][0] > max:
							max = color_struct[len(color_struct) - x - 1][0]
					# Leaving only the max. value
					for y in range(len(color_struct)):
						if color_struct[len(color_struct) - x - 1][0] != max:
							color_struct.pop(len(color_struct) - x - 1)
			except IndexError:
				print 'Using first value.'
	return color_struct

# This module reduces the yellow color structure when supposedly the 3 
# desired objects were detected.	
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
			if x == color_len - 1 and len(color_struct) > 3:
				color_struct = [color_struct[0],color_struct[1],\
				color_struct[2]]
				#for y in range(len(color_struct)):
					#if color_struct[len(color_struct) - x - 1][0] > max:
					#	max = color_struct[len(color_struct) - x - 1][0]
				
				for y in range(len(color_struct)):
					if color_struct[len(color_struct) - x - 1][0] != max:
						color_struct.pop(len(color_struct) - x - 1)
			'''
	# If there are more than 3 objects, leave the first three of them
	if len(color_struct) > 3:
		color_struct = [color_struct[0],color_struct[1],\
		color_struct[2]]
	
	return color_struct

# This module counts the number of pixels and gets some object data
# if supposedly only the desired objects were detected. When it finishes
# the image scan, it saves the data into a structure
def color_det_count(colours, rel_minix, rel_miniy, rel_maxix, rel_maxiy,\
opening_red, opening_green, opening_blue):

	width, height = opening_red.shape
	pixels_red, pixels_green, pixels_blue = 0, 0, 0
	cumulative_x_red, cumulative_x_green, cumulative_x_blue = 0, 0, 0
	cumulative_y_red, cumulative_y_green, cumulative_y_blue = 0, 0, 0
	minx_red, miny_red, maxx_red, maxy_red = 0, 0, 0, 0
	minx_green, miny_green, maxx_green, maxy_green = 0, 0, 0, 0
	minx_blue, miny_blue, maxx_blue, maxy_blue = 0, 0, 0, 0

	# Getting color data
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
			# Red
			if opening_red[x,y] > 0:
				pixels_red += 1			# Counting pixels
				cumulative_x_red += x	# Increasing cumulative
				cumulative_y_red += y	# Increasing cumulative
				# Getting limits
				minx_red, miny_red, maxx_red, maxy_red = limits(
				x,y,minx_red,miny_red,maxx_red,maxy_red)
		
			# Green
			if opening_green[x,y] > 0:
				pixels_green += 1		# Counting pixels
				cumulative_x_green += x	# Increasing cumulative
				cumulative_y_green += y	# Increasing cumulative
				# Getting limits
				minx_green, miny_green, maxx_green, maxy_green = limits(
				x,y,minx_green,miny_green,maxx_green,maxy_green)
			
			#Blue
			if opening_blue[x,y] > 0:
				pixels_blue += 1		# Counting pixels
				cumulative_x_blue += x	# Increasing cumulative
				cumulative_y_blue += y	# Increasing cumulative
				# Getting limits
				minx_blue, miny_blue, maxx_blue, maxy_blue = limits(
				x,y,minx_blue,miny_blue,maxx_blue,maxy_blue)

	# Assigning data to color structure
	# Red
	colours[0] = assignment(colours[0], minx_red, miny_red, maxx_red, maxy_red,
	pixels_red, cumulative_x_red, cumulative_y_red)
	
	# Green
	colours[1] = assignment(colours[1], minx_green, miny_green, maxx_green, maxy_green,
	pixels_green, cumulative_x_green, cumulative_y_green)
	
	# Blue
	colours[2] = assignment(colours[2], minx_blue, miny_blue, maxx_blue, maxy_blue,
	pixels_blue, cumulative_x_blue, cumulative_y_blue)
	
	return colours

# This module, instead of counting pixels per "layer", it applies the 
# DFS module to gather data, because supposedly more than 1 object was 
# detected. It then reduces each color list and makes an structure
# with the remaining data.
def color_det_dfs(colours, rel_minix, rel_miniy, rel_maxix, rel_maxiy, \
opening_red, opening_green, opening_blue):

	width, height = opening_red.shape
	red_counter, green_counter, blue_counter = 0, 0, 0
	red_colors, green_colors, blue_colors = [], [], []
	red_labels = np.zeros((width,height), np.uint8)
	green_labels = np.zeros((width,height), np.uint8)
	blue_labels = np.zeros((width,height), np.uint8)
	cumulatives = 0
	limits = 0
	
	# Getting color data
	rel_minix, rel_miniy, rel_maxix, rel_maxiy = 0, 0, 0, 0
	for y in range(height):
		row = opening_red[:,y]
		#print row
		max_row = max(row)
		if max_row > 0:
			if rel_maxiy == 0 and rel_miniy == 0:
				#rel_maxix, rel_minix = x, x
				rel_maxiy, rel_miniy = y, y
			else:
				if y > rel_maxiy:
					rel_maxiy = y
					
	for x in range(width):
		col = opening_red[x,:]
		max_col = max(col)
		if max_col > 0:
			if rel_maxix == 0 and rel_minix == 0:
				rel_maxix, rel_minix = x, x
				#rel_maxiy, rel_miniy = y, y
			else:
				if x > rel_maxix:
					rel_maxix = x
	#print rel_minix, rel_miniy, rel_maxix, rel_maxiy
	
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
			
			if opening_red[x,y] > 0 and red_labels[x,y] == 0:
				red_labels, red_counter, pixels, cumulatives, limits = DFS2(opening_red, 
				red_labels, x, y, red_counter)
			
				red_colors.append([pixels, cumulatives[0]/pixels, cumulatives[1]/pixels,
				limits[0], limits[1], limits[2], limits[3]])
				#print 'red', red_colors
				
	rel_minix, rel_miniy, rel_maxix, rel_maxiy = 0, 0, 0, 0
	for y in range(height):
		row = opening_green[:,y]
		#print row
		max_row = max(row)
		if max_row > 0:
			if rel_maxiy == 0 and rel_miniy == 0:
				#rel_maxix, rel_minix = x, x
				rel_maxiy, rel_miniy = y, y
			else:
				if y > rel_maxiy:
					rel_maxiy = y
					
	for x in range(width):
		col = opening_green[x,:]
		max_col = max(col)
		if max_col > 0:
			if rel_maxix == 0 and rel_minix == 0:
				rel_maxix, rel_minix = x, x
				#rel_maxiy, rel_miniy = y, y
			else:
				if x > rel_maxix:
					rel_maxix = x
	#print rel_minix, rel_miniy, rel_maxix, rel_maxiy
	
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
		
			if opening_green[x,y] > 0 and green_labels[x,y] == 0:
				green_labels, green_counter, pixels, cumulatives, limits = DFS2(opening_green, 
				green_labels, x, y, green_counter)
			
				green_colors.append([pixels, cumulatives[0]/pixels, cumulatives[1]/pixels,
				limits[0], limits[1], limits[2], limits[3]])
				#print 'green', green_colors
				
	rel_minix, rel_miniy, rel_maxix, rel_maxiy = 0, 0, 0, 0
	for y in range(height):
		row = opening_blue[:,y]
		#print row
		max_row = max(row)
		if max_row > 0:
			if rel_maxiy == 0 and rel_miniy == 0:
				#rel_maxix, rel_minix = x, x
				rel_maxiy, rel_miniy = y, y
			else:
				if y > rel_maxiy:
					rel_maxiy = y
					
	for x in range(width):
		col = opening_blue[x,:]
		max_col = max(col)
		if max_col > 0:
			if rel_maxix == 0 and rel_minix == 0:
				rel_maxix, rel_minix = x, x
				#rel_maxiy, rel_miniy = y, y
			else:
				if x > rel_maxix:
					rel_maxix = x
	#print rel_minix, rel_miniy, rel_maxix, rel_maxiy
	
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
	
			if opening_blue[x,y] > 0 and blue_labels[x,y] == 0:
				blue_labels, blue_counter, pixels, cumulatives, limits = DFS2(opening_blue, 
				blue_labels, x, y, blue_counter)
			
				blue_colors.append([pixels, cumulatives[0]/pixels, cumulatives[1]/pixels,
				limits[0], limits[1], limits[2], limits[3]])
				#print 'blue', blue_colors
	'''
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
			# Getting data with DFS2 and appending to auxiliary list
			# Red
			if opening_red[x,y] > 0 and red_labels[x,y] == 0:
				red_labels, red_counter, pixels, cumulatives, limits = \
				DFS2(opening_red, red_labels, x, y, red_counter)
			
				red_colors.append([pixels, cumulatives[0]/pixels, \
				cumulatives[1]/pixels, limits[0], limits[1], limits[2],\
				limits[3]])
		
			# Green
			if opening_green[x,y] > 0 and green_labels[x,y] == 0:
				green_labels, green_counter, pixels, cumulatives, limits = \
				DFS2(opening_green, green_labels, x, y, green_counter)
			
				green_colors.append([pixels, cumulatives[0]/pixels, \
				cumulatives[1]/pixels, limits[0], limits[1], limits[2],\
				limits[3]])
				
			# Blue
			if opening_blue[x,y] > 0 and blue_labels[x,y] == 0:
				blue_labels, blue_counter, pixels, cumulatives, limits = \
				DFS2(opening_blue, blue_labels, x, y, blue_counter)
			
				blue_colors.append([pixels, cumulatives[0]/pixels, \
				cumulatives[1]/pixels, limits[0], limits[1], limits[2],\
				limits[3]])
	'''
	# Popping small or large undesirable objects on each color structure
	# and keeping the biggest one of the remainders
	# Red
	#print red_colors
	red_colors = reducing_color(red_colors)
	
	# Green
	#print green_colors
	green_colors = reducing_color(green_colors)
	
	# Blue
	#print blue_colors
	blue_colors = reducing_color(blue_colors)
	
	# Reducing lists, if needed and assigning color data to list
	# Red
	#print 'red:',red_colors
	if len(red_colors) > 0:
		minx_red, miny_red, maxx_red, maxy_red = red_colors[0][3],\
		red_colors[0][4], red_colors[0][5], red_colors[0][6]
		pixels_red = red_colors[0][0]
		center = []
		center.append(red_colors[0][1])
		center.append(red_colors[0][2])
	else:
		minx_red, miny_red, maxx_red, maxy_red = 0, 0, 0, 0
		pixels_red, center = 0, [0,0]
	colours[0] = assignment2(colours[0], minx_red, miny_red, maxx_red, maxy_red,
	pixels_red, center)
	#print colours[0]._center_mass
	
	# Green
	#print 'green:',green_colors
	if len(green_colors) > 0:
		minx_green, miny_green, maxx_green, maxy_green = green_colors[0][3],\
		green_colors[0][4], green_colors[0][5], green_colors[0][6]
		pixels_green = green_colors[0][0]
		center = []
		center.append(green_colors[0][1])
		center.append(green_colors[0][2])
	else:
		minx_green, miny_green, maxx_green, maxy_green = 0, 0, 0, 0
		pixels_green, center = 0, [0,0]
	colours[1] = assignment2(colours[1], minx_green, miny_green, maxx_green, maxy_green,
	pixels_green, center)
	#print colours[1]._center_mass 
	
	# Blue
	#print 'blue:', blue_colors
	if len(blue_colors) > 0:
		minx_blue, miny_blue, maxx_blue, maxy_blue = blue_colors[0][3],\
		blue_colors[0][4], blue_colors[0][5], blue_colors[0][6]
		pixels_blue = blue_colors[0][0]
		center = []
		center.append(blue_colors[0][1])
		center.append(blue_colors[0][2])
	else:
		minx_blue, miny_blue, maxx_blue, maxy_blue = 0, 0, 0, 0
		pixels_blue, center = 0, [0,0]
	colours[2] = assignment2(colours[2], minx_blue, miny_blue, maxx_blue, maxy_blue,
	pixels_blue, center)
	#print colours[2]._center_mass
	
	return colours

# This module applies DFS to count the supposedly 3 detected yellow
# objects.	
def yellow_det_count(yellow_colours, rel_minix, rel_miniy, rel_maxix, \
rel_maxiy, opening_yellow,colours):
	
	width, height = opening_yellow.shape
	yellow_counter = 0
	yellow_labels = np.zeros((width,height), np.uint8)
	pixels_1, pixels_2, pixels_3 = 0, 0, 0
	cumulative_x_1, cumulative_x_2, cumulative_x_3 = 0, 0, 0
	cumulative_y_1, cumulative_y_2, cumulative_y_3 = 0, 0, 0
	minx_1, miny_1, maxx_1, maxy_1 = 0, 0, 0, 0
	minx_2, miny_2, maxx_2, maxy_2 = 0, 0, 0, 0
	minx_3, miny_3, maxx_3, maxy_3 = 0, 0, 0, 0
	data = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
	#vals = [0,0,0,0,0,0,0]
	#for a in range(len(colours)):
	#	data.append(vals)
		
	for a in range(len(colours)):
		#print data[a]
		difx = colours[a]._maxx - colours[a]._minx
		dify = colours[a]._maxy - colours[a]._miny
		center = colours[a]._center_mass
		#print center
		offset = 0.1
		multiplier = 1.5
		rel_miniy = int(center[1] - ((multiplier + offset) * dify))
		rel_maxiy = int(center[1] + ((multiplier + offset) * dify))
		rel_minix = int(center[0] - ((multiplier + offset) * difx))
		rel_maxix = int(center[0] + ((multiplier + offset) * difx))
		
		try:
			for y in range(rel_miniy, rel_maxiy):
				for x in range(rel_minix, rel_maxix):
					if opening_yellow[x,y] > 0:
						data[a][0] += 1	# Num. of pixels
						#print 'inside'
						data[a][1] += x	# Cumulative x
						data[a][2] += y	# Cumulative y
						
						if data[a][3] == 0 and data[a][5] == 0 and \
							data[a][4] == 0 and data[a][6] == 0:
							data[a][3], data[a][4] = x, x
							data[a][5], data[a][6] = y, y
						else:
							if x < data[a][3]:		# min x
								data[a][3] = x
							elif x > data[a][4]:	# max x
								data[a][4] = x
							if y < data[a][5]:		# min y
								data[a][5] = y
							elif y > data[a][6]:	# max y 
								data[a][6] = y
		except IndexError:
			data[a] = [0,0,0,0,0,0,0]
	#print data
	#print data[0]
	pixels_1, cumulative_x_1, cumulative_y_1, minx_1, maxx_1, \
	miny_1, maxy_1 = data[0][:]
	#print data[1]
	pixels_2, cumulative_x_2, cumulative_y_2, minx_2, maxx_2, \
	miny_2, maxy_2 = data[1][:]
	#print data[2]
	pixels_3, cumulative_x_3, cumulative_y_3, minx_3, maxx_3, \
	miny_3, maxy_3 = data[2][:]
	'''
	# Applying DFS
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
			if opening_yellow[x,y] > 0 and yellow_labels[x,y] == 0:
				yellow_labels, yellow_counter = DFS(opening_yellow,\
				yellow_labels, x, y, yellow_counter)
				
	# Getting limits of yellow colors
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
			
			if yellow_labels[x,y] == 1:
				pixels_1 += 1
				cumulative_x_1 += x
				cumulative_y_1 += y
				#minx_1, miny_1, maxx_1, maxy_1 = limits(
				#x,y,minx_1,miny_1,maxx_1,maxy_1)
				if minx_1 == 0 and miny_1 == 0 and \
					maxx_1 == 0 and maxy_1 == 0:
					minx_1, maxx_1 = x, x
					miny_1, maxy_1 = y, y
				else:
					if x < minx_1:
						minx_1 = x
					elif x > maxx_1:
						maxx_1 = x
					if y < miny_1:
						miny_1 = y
					elif y > maxy_1:
						maxy_1 = y
			
			if yellow_labels[x,y] == 2:
				pixels_2 += 1
				cumulative_x_2 += x
				cumulative_y_2 += y
				#minx_2, miny_2, maxx_2, maxy_2 = limits(
				#x,y,minx_2,miny_2,maxx_2,maxy_2)
				if minx_2 == 0 and miny_2 == 0 and \
					maxx_2 == 0 and maxy_2 == 0:
					minx_2, maxx_2 = x, x
					miny_2, maxy_2 = y, y
				else:
					if x < minx_2:
						minx_2 = x
					elif x > maxx_2:
						maxx_2 = x
					if y < miny_2:
						miny_2 = y
					elif y > maxy_2:
						maxy_2 = y
			
			if yellow_labels[x,y] == 3:
				pixels_3 += 1
				cumulative_x_3 += x
				cumulative_y_3 += y
				#minx_3, miny_3, maxx_3, maxy_3 = limits(
				#x,y,minx_3,miny_3,maxx_3,maxy_3)
				if minx_3 == 0 and miny_3 == 0 and \
					maxx_3 == 0 and maxy_3 == 0:
					minx_3, maxx_3 = x, x
					miny_3, maxy_3 = y, y
				else:
					if x < minx_3:
						minx_3 = x
					elif x > maxx_3:
						maxx_3 = x
					if y < miny_3:
						miny_3 = y
					elif y > maxy_3:
						maxy_3 = y
	'''
	# Assigning data to structure
	# Yellow 1
	yellow_colours[0] = assignment(yellow_colours[0], minx_1, miny_1, maxx_1, 
	maxy_1, pixels_1, cumulative_x_1, cumulative_y_1)
	#print yellow_colours[1]._center_mass 
	# Yellow 2
	yellow_colours[1] = assignment(yellow_colours[1], minx_2, miny_2, maxx_2, 
	maxy_2, pixels_2, cumulative_x_2, cumulative_y_2)
	#print yellow_colours[1]._center_mass 
	# Yellow 3
	yellow_colours[2] = assignment(yellow_colours[2], minx_3, miny_3, maxx_3, 
	maxy_3, pixels_3, cumulative_x_3, cumulative_y_3)
	#print yellow_colours[2]._center_mass
	
	return yellow_colours

# This module applies the DFS2 to gather the data of multiple objects
def yellow_det_dfs(yellow_colours, rel_minix, rel_miniy, rel_maxix, rel_maxiy, \
opening_yellow):

	width, height = opening_yellow.shape
	yellow_counter = 0
	yellow_labels = np.zeros((width,height), np.uint8)
	yellow_colors2 = []
	first = 0
	yellow_pixels = 0
	cumulatives_yellow = 0
	limits_yellow = 0
	
	# Applying DFS2 and gathering needed data
	for y in range(rel_miniy, rel_maxiy):
		for x in range(rel_minix, rel_maxix):
			if opening_yellow[x,y] > 0 and yellow_labels[x,y] == 0:

				yellow_labels, yellow_counter, yellow_pixels, \
				cumulatives_yellow, limits_yellow = DFS2(opening_yellow,\
				yellow_labels, x, y, yellow_counter)
				
				yellow_colors2.append([yellow_pixels, 
				cumulatives_yellow[0]/yellow_pixels, cumulatives_yellow[1]/yellow_pixels, 
				limits_yellow[0], limits_yellow[1], limits_yellow[2], 
				limits_yellow[3]])

	
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
	
	# Reducing yellow color structure
	yellow_colors2 = reducing_yellow(yellow_colors2)

	# Assigning color data to list
	for x in range(len(yellow_colors2)):
		# Yellow 1
		if len(yellow_colors2) > 0:
			minx_yellow, miny_yellow, maxx_yellow, maxy_yellow = yellow_colors2[x][3],\
			yellow_colors2[x][4], yellow_colors2[x][5], yellow_colors2[x][6]
			pixels_yellow = yellow_colors2[x][0]
			center = []
			center.append(yellow_colors2[x][1])
			center.append(yellow_colors2[x][2])
		else:
			minx_yellow, miny_yellow, maxx_yellow, maxy_yellow = 0, 0, 0, 0
			pixels_yellow, center = 0, [0,0]
			
		yellow_colours[x] = assignment2(yellow_colours[x], minx_yellow, \
		miny_yellow, maxx_yellow, maxy_yellow,
		pixels_yellow, center)
		#print yellow_colors[0]._center_mass
	
	return yellow_colours
	
def robot_detection():
	# Connecting pc with NXT robot via bluetooth 
	#brick = nxt.locator.find_one_brick(name = 'NXT1')
	#robot = Robot(brick)
	
	# Bluetooth connection with arduino
	ser = serial.Serial(12, 9600, timeout = 1)
	
	# Getting thresholds from file
	try:
		file = open(default.file_name, 'r')
		thr = read_thres(file)
	except IOError, ErrorValue:
		print 'File not found or corrupted. Using defaults.'
		thr = default.def_vals
	
	timez = 0
	# Starting time counter to measure elapsed time
	e1 = cv2.getTickCount()
	
	# Choosing camera to work with
	cap = cv2.VideoCapture(default.cam_num)
	
	while(True):
		# Reading capture from chosen camera
		ret, img = cap.read()
		
		# If it has an image
		if(ret):
			# Number of robots
			bot_num = 3
			
			# Colors structure
			colors = []
			for x in range(bot_num):
				colors.append(circle_data())
			
			# Open image manually, used for tests
			#img_name = 'pic18.png'
			#img = cv2.imread(img_name)
			width, height,depth = img.shape
			#print width, height

			# RGB to HSV transformation
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

			# Colors. (Thresholds for binarization)
			# Red seems to work better with 2 thresholds
			red_low2 = np.array([thr[0], thr[1], thr[2]])
			red_up2 = np.array([thr[3], thr[4], thr[5]])
			red_low3 = np.array([thr[6], thr[7], thr[8]])
			red_up3 = np.array([thr[9], thr[10], thr[11]])

			green_low = np.array([thr[12], thr[13], thr[14]])
			green_up = np.array([thr[15], thr[16], thr[17]])

			blue_low = np.array([thr[18], thr[19], thr[20]])
			blue_up = np.array([thr[21], thr[22], thr[23]])

			yellow_low = np.array([thr[24], thr[25], thr[26]])
			yellow_up = np.array([thr[27], thr[28], thr[29]])

			# Thresholding the HSV images
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
			
			# Applying Opening operation (Erode then dilate)
			kernel = np.ones((5,5),np.uint8)
			#erode_img = cv2.erode(img,kernel,iterations=2)
			red_opening2 = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel)
			green_opening2 = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
			blue_opening2 = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
			yellow_opening2 = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel)
			#color_glb_opening2 = cv2.morphologyEx(color_global, cv2.MORPH_OPEN, kernel)
			
			# Dilating images to recover and approx. original size
			red_opening = cv2.dilate(red_opening2, kernel, iterations=1)
			green_opening = cv2.dilate(green_opening2, kernel, iterations=1)
			blue_opening = cv2.dilate(blue_opening2, kernel, iterations=1)
			yellow_opening = cv2.dilate(yellow_opening2, kernel, iterations=1)
			#color_glb_opening = cv2.dilate(color_glb_opening2, kernel, iterations=2)
			
			# Images mixed. This is latter used to get relative boundaries
			# to save time in future processes
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
			
			# Getting max and min relative values for further 
			# image processing. Instead of scanning the whole image,
			# it'll only scan the area of interest.

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
			
			# If colors are detected correctly (Boundaries less than
			# a quarter of the image) it only counts the pixels. If not,
			# it applies DFS
			if (rel_maxy - rel_miny) < height / 4 and \
			(rel_maxx - rel_minx) < width / 4:
				
				colors = color_det_count(colors, rel_minx, rel_miny, rel_maxx, \
				rel_maxy, red_opening, green_opening, blue_opening)
				
			else:
				
				colors = color_det_dfs(colors, rel_minx, rel_miny, rel_maxx, rel_maxy, \
				red_opening, green_opening, blue_opening)
				
			# Showing centers of mass on a new image and bounding boxes
			img2 = img
			#img2 = cv2.imread(img_name)
			color = (0,255,0)
			for x in range(len(colors)):
				#print colors[x]._minx, colors[x]._miny, colors[x]._maxx, \
				#colors[x]._maxy
				img2[colors[x]._center_mass[0], colors[x]._center_mass[1]] = (0,255,0)
				img2 = print_box(img2,colors[x],color)
			
			# Colors structure
			yellow_colors = []
			for x in range(bot_num):
				yellow_colors.append(circle_data())

			# If colors are detected correctly (Boundaries less than
			# a quarter of the image) it only applies DFS. If not,
			# it applies DFS2 to get rid of undesired objects
			if (rel_maxy - rel_miny) < height / 4 and \
			(rel_maxx - rel_minx) < width / 4:
				
				yellow_colors = yellow_det_count(yellow_colors, rel_minx, rel_miny, \
				rel_maxx, rel_maxy, yellow_opening, colors)
				
			else:
			
				#yellow_colors = yellow_det_dfs(yellow_colors, rel_minx, rel_miny, \
				#rel_maxx, rel_maxy, yellow_opening)
				yellow_colors = yellow_det_count(yellow_colors, rel_minx, rel_miny, \
				rel_maxx, rel_maxy, yellow_opening, colors)
			
			# Showing centers of mass on a new image and bounding boxes
			#img2 = cv2.imread('equ_3.png')
			color = (0,255,255)
			#print len(yellow_colors)
			#print yellow_colors
			for x in range(len(yellow_colors)):
				#print yellow_colors[x]._minx, yellow_colors[x]._miny, yellow_colors[x]._maxx, \
				#yellow_colors[x]._maxy
				if len(yellow_colors[x]._center_mass) == 0:
					yellow_colors[x]._center_mass = [width / 2 , height / 2]
				else:
					img2[yellow_colors[x]._center_mass[0], yellow_colors[x]._center_mass[1]] = (0,255,255)
					img2 = print_box(img2,yellow_colors[x],color)
			
			#cv2.imshow('center of mass',img2)
			#cv2.waitKey(0)
			
			# Choosing which yellow color corresponds to which color(
			# red, green, blue) and calculating orientation
			font = cv2.FONT_HERSHEY_SIMPLEX # Font used to write on result image
			minimum = 0
			#distances = []
			# Getting the euclidean distance between the centers of mass
			for x in range(len(yellow_colors)):
				distances = []
				xy_vals = []
				
				for y in range(len(colors)):
					#print x, y
					distance = euclidean_dist(yellow_colors[x]._center_mass, 
					colors[y]._center_mass)
					distances.append(distance)
					x_val = -yellow_colors[x]._center_mass[0] + \
					colors[y]._center_mass[0]
					y_val = -(height - yellow_colors[x]._center_mass[1]) + \
					(height - colors[y]._center_mass[1])
					xy_vals.append([x_val, y_val])
				
				# Choosing the minimum distance and calculating the 
				# Orientation in degrees
				minimum = min(distances)
				for z in range(len(distances)):
					if minimum == distances[z]:
						#print distances[z]
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
						if distances[z] <= 50:
							cv2.putText(img2,str(int(angle_deg)),(b,a),font,0.75,
							(255,255,255),1)
						else:
							cv2.putText(img2,'Color not detected',(0,20),font,0.5,
							(255,255,255),1)
			
			row = 35
			farben = ['R = ', 'G = ', 'B = ']
			# Printing positions (in pixels) on image (row, column)
			for x in range(len(colors)):
				cv2.putText(img2,farben[x] + str(colors[x]._center_mass),(15,row),font,0.75,
								(255,255,255),1)
				row += 20
				
				
			# Printing boundaries by getting biggest area
			#areas = []
			#area = 0
			h, w, max_area, indx, area= 0, 0, 0, 0, 0
			for x in range(len(colors)):
				h = colors[x]._maxy - colors[x]._miny
				w = colors[x]._maxx - colors[x]._minx
				#areas.append(h*w)
				area = h * w
				if area > max_area:
					indx = x
			#miny, maxy, minx, maxx = 0,0,0,0
			miny = 0 + (colors[indx]._maxy - colors[indx]._miny)
			minx = 0 + (colors[indx]._maxx - colors[indx]._minx)
			maxy = height - (colors[indx]._maxy - colors[indx]._miny)
			maxx = width - (colors[indx]._maxx - colors[indx]._minx)
			
			cv2.rectangle(img2,(minx,miny),(maxy,maxx),(0,0,255),1)
			
			e2 = cv2.getTickCount() # Getting time after processing
			# Calculating elapsed time
			time = (e2 - e1) / cv2.getTickFrequency()
			print time - timez
			timez = time
			# Showing result image
			cv2.imshow('center of mass',img2)
			#cv2.waitKey(0)
			# Press "q" (quit) to exit
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			ser.write(str(colors[1]._orientation)+'\n')
			'''
			# Moving robot according to the detected angle
			if colors[1]._orientation >= 0 and colors[1]._orientation <= 100:
				m_left = Motor(brick, PORT_B)
				m_left.turn(100, 90)
			elif colors[1]._orientation >= 270 and colors[1]._orientation <= 359:
				m_right = Motor(brick, PORT_B)
				m_right.turn(-100, 90)
			'''
	
	ser.close()	# Closing serial communication
	cap.release() # Releasing capture
	cv2.destroyAllWindows()

# This module only shows the real time captures of the camera
def show_cam():
	# Selecting camera
	cap = cv2.VideoCapture(default.cam_num)

	while(True):
		# Capture frame
		ret, frame = cap.read()

		# Showing frame, press q(quit) to exit
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Releasing capture
	cap.release()
	cv2.destroyAllWindows()

def write_new_vals(color,hmini,smini,vmini,hmaxi,smaxi,vmaxi,file1):
	with file1 as f:
		lines = f.readlines()
		
	# Writing values
	for y in range(len(lines)):
		if lines[y] == color:
			for z in range(y,len(lines)):
				print 'equal'
				if lines[z] == 'low\n':
					lines[z+1] = 'h=' + str(hmini) + '\n'
					lines[z+2] = 's=' + str(smini) + '\n'
					lines[z+3] = 'v=' + str(vmini) + '\n'
				
				if lines[z] == 'up\n':
					lines[z+1] = 'h=' + str(hmaxi) + '\n'
					lines[z+2] = 's=' + str(smaxi) + '\n'
					lines[z+3] = 'v=' + str(vmaxi) + '\n'
					break
	#file1.close()

	file1 = open(default.file_name, 'w')
	with file1 as f:
		f.writelines(lines)
	
# Module used in thres_adj	
def nothing(x):
	pass

# This module helps choosing the needed thresholds by applying 
# thresholds via sliders and showing the result images

def thres_adj():

	# Creating window
	cv2.namedWindow('sliders')

	# create trackbars for color change
	cv2.createTrackbar('Hmin','sliders',0,179,nothing)
	cv2.createTrackbar('Smin','sliders',0,255,nothing)
	cv2.createTrackbar('Vmin','sliders',0,255,nothing)

	cv2.createTrackbar('Hmax','sliders',179,179,nothing)
	cv2.createTrackbar('Smax','sliders',255,255,nothing)
	cv2.createTrackbar('Vmax','sliders',255,255,nothing)
	
	# Creating window
	cv2.namedWindow('save data')
	#saving = '0 : Nothing \n1 : Save'
	cv2.createTrackbar('save','save data',0,1,nothing)
	#colors_used = '0 : red2 \n1 : red3 \n2 : green \n3 : blue \n4 : yellow '
	cv2.createTrackbar('r2r3gby','save data',0,4,nothing)

	# Choosing camera
	cap = cv2.VideoCapture(default.cam_num)

	while(True):
		ret, img = cap.read()
		# If there is a capture
		if(ret):
			# RGB to HSV transformation
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			
			# Get current positions of four trackbars
			hmin = cv2.getTrackbarPos('Hmin','sliders')
			smin = cv2.getTrackbarPos('Smin','sliders')
			vmin = cv2.getTrackbarPos('Vmin','sliders')
			hmax = cv2.getTrackbarPos('Hmax','sliders')
			smax = cv2.getTrackbarPos('Smax','sliders')
			vmax = cv2.getTrackbarPos('Vmax','sliders')
			
			# Low and up thresholds. Values from trackbars
			low = np.array([hmin, smin, vmin])
			up = np.array([hmax, smax, vmax])

			# Thresholding the HSV image
			mask = cv2.inRange(hsv, low, up)

			# Showing binary image
			cv2.imshow('mask',mask)
			# Press "q" to exit
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			# Applying opening operation
			kernel = np.ones((5,5),np.uint8) # Square kernel matrix
			#erode_img = cv2.erode(mask,kernel,iterations=2)
			opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
			cv2.imshow('open',opening)
			# Press "q" to exit
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			# Getting trackbar positions to choose whether to save
			# or not
			get_save = cv2.getTrackbarPos('save','save data')
			#print get_save
			get_color = cv2.getTrackbarPos('r2r3gby','save data')
			
			if get_save == 1:
				# Getting thresholds from file
				try:
					file = open(default.file_name, 'r')
					colour = default.colors_used[get_color]
					#print colour
					write_new_vals(colour,hmin,smin,vmin,hmax,smax,
					vmax,file)
					#time.sleep(500)
					#print 'time elapsed'
					# Resetting
					cv2.createTrackbar('save','save data',0,1,nothing)
				except IOError, ErrorValue:
					print 'File not found or corrupted. Please, \
					place a working file in project folder.'
				
	# Releasing capture
	cap.release()
	cv2.destroyAllWindows()

# This module reads a line from a target file
def read_line_thres(lines2, y2,thres):
	h, s, v = '', '', ''
	for a in range(2,len(lines2[y2+2])):
		if lines2[y2+2][a] == '\n':
			break
		h += lines2[y2+2][a]
	#print 'h=' , int(h)
	thres.append(int(h))
	
	for a in range(2,len(lines2[y2+3])):
		if lines2[y2+3][a] == '\n':
			break
		s += lines2[y2+3][a]
	#print 's=' , int(s)
	thres.append(int(s))
	
	for a in range(2,len(lines2[y2+4])):
		if lines2[y2+4][a] == '\n':
			break
		v += lines2[y2+4][a]
	#print 'v=' , int(v)
	thres.append(int(v))
	
	return thres

# This module reads a target file in the same project folder	
def read_thres(file1):
	color_thres = default.colors_used
	with file1 as f:
		lines = f.readlines()

	up = 'up\n'
	low = 'low\n'
	thresholds = []	

	for x in range(len(color_thres)):
		for y in range(len(lines)):
			first = 0
			if lines[y] == color_thres[x]:
				if lines[y+1] == low and lines[y] == color_thres[x]:

					thresholds = read_line_thres(lines, y, thresholds)

				if lines[y+1] == up and lines[y] == color_thres[x]:
					thresholds = read_line_thres(lines, y, thresholds)
					break

	return thresholds

# This Module reads the units used in pixels/cm from a text file
def read_units(file1):
	
	with file1 as f:
		lines = f.readlines()

	unit = 'units\n'

	for x in range(len(lines)):
		if lines[x] == unit:
			unit_val = int(lines[x+1])
			break
		
	return unit_val

# This Module reads the units used in pixels/cm from a text file
def write_units(file1,unit_val):
	
	with file1 as f:
		lines = f.readlines()

	unit = 'units\n'

	for x in range(len(lines)):
		if lines[x] == unit:
			lines[x+1] = str(unit_val) + '\n'
			break
	
	file1 = open(default.file_name, 'w')
	with file1 as f:
		f.writelines(lines)
	
# This module shows the binary images with the current thresholds	
def show_hsv_binary():
	# Choosing camera
	cap = cv2.VideoCapture(default.cam_num)

	# Getting thresholds from file
	try:
		file = open(default.file_name, 'r')
		thr = read_thres(file)
		#file = open(default.file_name, 'r') # Reopen file
		#value_units = read_units(file)
		print value_units
	except IOError, ErrorValue:
		print 'File not found or corrupted. Using defaults.'
		thr = default.def_vals

	while(True):
		# Capture frame
		ret, frame = cap.read()
		
		# If there is an image
		if(ret):

			# Size of frame
			width, height,depth = frame.shape
			#print width, height

			# RGB to HSV transformation
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			
			# Colors
			red_low2 = np.array([thr[0], thr[1], thr[2]])
			red_up2 = np.array([thr[3], thr[4], thr[5]])
			red_low3 = np.array([thr[6], thr[7], thr[8]])
			red_up3 = np.array([thr[9], thr[10], thr[11]])

			green_low = np.array([thr[12], thr[13], thr[14]])
			green_up = np.array([thr[15], thr[16], thr[17]])

			blue_low = np.array([thr[18], thr[19], thr[20]])
			blue_up = np.array([thr[21], thr[22], thr[23]])

			yellow_low = np.array([thr[24], thr[25], thr[26]])
			yellow_up = np.array([thr[27], thr[28], thr[29]])

			# Thresholding the HSV image
			#red = cv2.inRange(hsv, red_low, red_up)
			red = np.zeros((height,width,3), np.uint8)
			red2 = cv2.inRange(hsv, red_low2, red_up2)
			red3 = cv2.inRange(hsv, red_low3, red_up3)
			red = cv2.bitwise_or(red2, red3, red)
			green = cv2.inRange(hsv, green_low, green_up)
			blue = cv2.inRange(hsv, blue_low, blue_up)
			yellow = cv2.inRange(hsv, yellow_low, yellow_up)
			
			# Showing hsv binary images
			cv2.imshow('red',red)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			cv2.imshow('green',green)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			cv2.imshow('blue',blue)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			cv2.imshow('yellow',yellow)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	# Releasing the capture
	cap.release()
	cv2.destroyAllWindows()

def write_units(file1,diff):
	with file1 as f:
		lines = f.readlines()
		
	for x in range(len(lines)):
		if lines[x] == 'units\n':
			#lines[x+1] = val
			lines[x+2] = str(diff)+'\n'
			break
			
	file1 = open(default.file_name, 'w')
	with file1 as f:
		f.writelines(lines)
	
def units_selection():
	
	def callback(known_dist):
		#print e.get()
		#val = e.get()
		# Getting thresholds from file
		try:
			file = open(default.file_name, 'r')
			write_units(file,known_dist)
		except IOError, ErrorValue:
			print 'File not found or corrupted. Using defaults.'
		
	
	units = Tk()
	#e = Entry(units)
	#e.pack()
	#e.focus_set()

	# Creating window
	cv2.namedWindow('sliders')

	# create trackbars for color change
	cv2.createTrackbar('Hmin','sliders',0,179,nothing)
	cv2.createTrackbar('Smin','sliders',0,255,nothing)
	cv2.createTrackbar('Vmin','sliders',0,255,nothing)

	cv2.createTrackbar('Hmax','sliders',179,179,nothing)
	cv2.createTrackbar('Smax','sliders',255,255,nothing)
	cv2.createTrackbar('Vmax','sliders',255,255,nothing)
	'''
	# Creating window
	cv2.namedWindow('save units')
	#saving = '0 : Nothing \n1 : Save'
	cv2.createTrackbar('save','save units',0,1,nothing)
	#colors_used = '0 : red2 \n1 : red3 \n2 : green \n3 : blue \n4 : yellow '
	cv2.createTrackbar('r2r3gby','save units',0,4,nothing)
	'''
	# Choosing camera
	cap = cv2.VideoCapture(default.cam_num)

	while(True):
		ret, img = cap.read()
		# If there is a capture
		if(ret):
			# RGB to HSV transformation
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			
			# Get current positions of four trackbars
			hmin = cv2.getTrackbarPos('Hmin','sliders')
			smin = cv2.getTrackbarPos('Smin','sliders')
			vmin = cv2.getTrackbarPos('Vmin','sliders')
			hmax = cv2.getTrackbarPos('Hmax','sliders')
			smax = cv2.getTrackbarPos('Smax','sliders')
			vmax = cv2.getTrackbarPos('Vmax','sliders')
			
			# Low and up thresholds. Values from trackbars
			low = np.array([hmin, smin, vmin])
			up = np.array([hmax, smax, vmax])

			# Thresholding the HSV image
			mask = cv2.inRange(hsv, low, up)

			# Showing binary image
			cv2.imshow('mask',mask)
			# Press "q" to exit
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			# Applying opening operation
			kernel = np.ones((5,5),np.uint8) # Square kernel matrix
			#erode_img = cv2.erode(mask,kernel,iterations=2)
			opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
			cv2.imshow('open',opening)
			# Press "q" to exit
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			
			'''
			# Getting trackbar positions to choose whether to save
			# or not
			get_save = cv2.getTrackbarPos('save','save units')
			#print get_save
			get_color = cv2.getTrackbarPos('r2r3gby','save units')
			
			if get_save == 1:
				# Getting thresholds from file
				try:
					file = open(default.file_name, 'r')
					colour = default.colors_used[get_color]
					#print colour
					write_new_vals(colour,hmin,smin,vmin,hmax,smax,
					vmax,file)
					#time.sleep(500)
					#print 'time elapsed'
					# Resetting
					cv2.createTrackbar('save','save units',0,1,nothing)
				except IOError, ErrorValue:
					print 'File not found or corrupted. Please, \
					place a working file in project folder.'
			'''
	# Getting max and min relative values for further 
	# image processing. Instead of scanning the whole image,
	# it'll only scan the area of interest.
	width, height = opening.shape
	rel_minx, rel_miny, rel_maxx, rel_maxy = 0, 0, 0, 0
	for y in range(height):
		row = opening[:,y]
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
		col = opening[x,:]
		max_col = max(col)
		if max_col > 0:
			if rel_maxx == 0 and rel_minx == 0:
				rel_maxx, rel_minx = x, x
				#rel_maxy, rel_miny = y, y
			else:
				if x > rel_maxx:
					rel_maxx = x
	
	diffx = rel_maxx - rel_minx
	diffy = rel_maxy - rel_miny
	known_dist = 0
	
	if diffx > diffy:
		known_dist = diffx
	else:
		known_dist = diffy
	
	b = Button(units, text="get value", width=10, command=callback(known_dist))
	b.pack()	
	
	mainloop()
	#e = Entry(units, width=50)
	#e.pack()

	# Releasing capture
	cap.release()
	cv2.destroyAllWindows()
	
# Main function
if __name__ == "__main__":
	
	master = Tk() # Creating master control
	
	# It seems that tkinter supports only gif images
	icon=PhotoImage(file="qr.gif")
	
	# Creating buttons of master control to call the corresponding
	# functions.
	button_det = Button(master, compound = LEFT, image=icon, text="Start robot detection",command=robot_detection)
	button_det.pack()
	
	button_show = Button(master, text="Show camera image",  height=3, width=50 ,command=show_cam)
	button_show.pack()
	
	button_thres = Button(master, text="Threshold adjustment",  height=3, width=50 ,command=thres_adj)
	button_thres.pack()
	
	button_hsv = Button(master, text="Show hsv binary images",  height=3, width=50 ,command=show_hsv_binary)
	button_hsv.pack()
	
	button_units = Button(master, text="Units adjustment",  height=3, width=50 ,command=units_selection)
	button_units.pack()
	
	#button_quit = Button(master, text="QUIT", command=)
	#button_thres.pack()
	
	master.mainloop()
	