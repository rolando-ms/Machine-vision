from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
#from edge_detection import edge_detection
from object_detection_hw2 import object_detection
from PIL import Image
#from PIL import ImageFont # Use fonts
#from PIL import ImageDraw # Draw texts
import math
import numpy as np
#import time # to use time.sleep('time in seconds')
#import os # to construct a path relative to this script
import cv2 # Open cv library
#import matplotlib.pyplot as plt

#---------------------
# Line fitting module
#---------------------
# This module takes lists of points and then calculates its mean value
# and returns the initial and end points of the segment.

def linefitting(points, angles_rad):
	N = len(points)
	#angles_rad = angles_rad.load()
	width, height = angles_rad.shape
	#angles_new = Image.new('L', (width,height), "black")
	#angles_pix = angles_new.load()
	angles_pix = np.zeros((width,height), dtype = float)
	rho_angle_pairs = []
	repetitions = []
	rho_angle = []
	
	for a in range(N):
		# Adding 2 * pi to negative values
		if angles_rad[points[a][0],points[a][1]] < 0:
			angles_pix[points[a][0],points[a][1]] = \
			angles_rad[points[a][0],points[a][1]] + 2.0 * math.pi
		else:
			angles_pix[points[a][0],points[a][1]] = \
			angles_rad[points[a][0],points[a][1]]
		
		# If the angle == 5 (0 degrees)
		if angles_rad[points[a][0],points[a][1]] == 5:
			angles_pix[points[a][0],points[a][1]] = 0.0
		
		# Adding pi/2 (90 degrees; orthogonal vector)
		angles_pix[points[a][0],points[a][1]] += (math.pi / 2.0)
		if angles_pix[points[a][0],points[a][1]] > (2 * math.pi):
			angles_pix[points[a][0],points[a][1]] += (-math.pi / 2.0)
		
		if angles_pix[points[a][0],points[a][1]] > math.pi:
			angles_pix[points[a][0],points[a][1]] += (-math.pi)
		
		#print angles_pix[points[a][0],points[a][1]] #* (180/math.pi)
		#print points[a][0], points[a][1]
		#print angles_rad[points[a][0],points[a][1]]
		
		# Calculating sine and cosine of the angle
		sine = math.sin(angles_pix[points[a][0],points[a][1]])
		if (sine > 0.0 and sine < 0.000001) or \
		(sine < 0.0 and sine > -0.000001):
			sine = 0.0
		#print 'sin(theta) = ' , sine #* (180/math.pi)
		
		cosine = math.cos(angles_pix[points[a][0],points[a][1]])
		if (cosine > 0.0 and cosine < 0.000001) or \
		(cosine < 0.0 and cosine > -0.000001):
			cosine = 0.0
		#print 'cos(theta) = ' , cosine #* (180/math.pi)
		
		x = float(points[a][0])
		#print 'x= ', x
		y = float(points[a][1])
		#print 'y= ', y
		
		# Normal line equation
		rho_aux = int((x * cosine) + ((y) * sine)) #float(height) -  ; you need to deduct height in order to have a common xy coordinate system equation, if not you get the programming image equation (inverted y)
		
		#print rho_aux, ' = x * cos(',angles_pix[points[a][0],points[a][1]],\
		#') + y * sin(',angles_pix[points[a][0],points[a][1]],')'
		#, line_angle
		
		# Saving temporal rho-angle-pair
		rho_angle = [rho_aux, angles_pix[points[a][0],points[a][1]]]
		
		# Appending pairs into lists to choose the most repeated one
		if len(rho_angle_pairs) == 0:
			rho_angle_pairs.append(rho_angle)
			repetitions.append([1])
		else:
			for b in range(len(rho_angle_pairs)):
				if rho_angle == rho_angle_pairs[b]:
					#print rho_angle
					#print rho_angle_pairs
					#print b
					#print repetitions
					repetitions[b][0] += 1
					break
				else:
					if b == (len(rho_angle_pairs) - 1):
						rho_angle_pairs.append(rho_angle)
						repetitions.append([1])
						#print rho_angle[1] - math.pi
	
	# Choosing most repeated pair
	for a in range(len(rho_angle_pairs)):
		if max(repetitions) == repetitions[a]:
			rho_1 = rho_angle_pairs[b][0]
			angle_line = rho_angle_pairs[b][1]
	
	#print rho_1
	#print angle_line
	return angles_pix, rho_1, angle_line
	
# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'figures.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	objects, segment, angles_norm, objs_data, angle_rads = object_detection(img,pixels)
	#print objs_data[0]._sides
	#print segment[0]
	
	# Transforming PIL image to opencv image
	img2 = Image.open(imgspath + name).convert('RGB')
	lines_rgb = np.array(img2)
	lines = lines_rgb[:,:,::-1].copy()
	
	# Numpy array to store fitted lines
	width, height = objects.size
	#lines = np.zeros((height,width,3), np.uint8)
	z = 0
	# Taking all segments and running line fitting
	for x in range(len(segment)):
		print 'Line equations of object ', x
		for y in range(len(segment[x])):
			segment_points = segment[x][y]
			if len(segment_points) > 10 and objs_data[x]._sides != 0:
				angles_news, rho, angle_segment= linefitting(segment_points, angle_rads)
				print rho, ' = x * cos(',angle_segment,\
				') + y * sin(',angle_segment,')'
				x1 = 0
				y1 = int((rho - x1*math.cos(angle_segment)) / \
				math.sin(angle_segment))
				if y1 < 0 or y1 > 10000:
					y1 = 0
					#print segment_points[0]
					x1 = int(segment_points[0][0]) # Taking first x value
				inipoint = (x1,y1)
				#print inipoint
				x2 = 300
				y2 = int((rho - x2*math.cos(angle_segment)) / \
				math.sin(angle_segment))
				if y2 < 0 or y2 > 10000:
					y2 = height
					x2 = x1
				endpoint = (x2,y2)
				#print endpoint
				#inipoint, endpoint = linefitting(segment_points, angles_rads)
				# Drawing fitted lines into lines array 
				#if x == 3 or x == 0:
				cv2.line(lines, inipoint, endpoint,(z,z,255),1)
		z += 40
	'''
	angles_pixs = angles_news.load()
	angles_new2 = Image.new('RGB', (width,height), "black")
	angles_pix2 = angles_new2.load()
	for y in range(height):
		for x in range(width):
			if (angles_pixs[x,y] * (180/math.pi)) > 360:
				angles_pix2[x,y] = (255,0,0)
	'''
	print 'height = ', height
	print 'width = ', width
	#angles_new2.show()
	# Showing results
	objects.show()
	cv2.imshow('image',lines)
	cv2.waitKey(0)
	cv2.destroyAllWindows()