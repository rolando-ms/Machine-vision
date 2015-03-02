from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
#from edge_detection import edge_detection
from object_detection_hw2 import object_detection
from PIL import Image
#from PIL import ImageFont # Use fonts
#from PIL import ImageDraw # Draw texts
#import math
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

def linefitting(points, angles):

	# Initializing values
	sumx, sumy, sumxx, sumyy, sumxy = 0.0, 0.0, 0.0, 0.0, 0.0 
	N, initial, end = 0.0, 0.0, 0.0
	partial_segmentx, partial_segmenty = 0.0, 0.0
	mean_point = [0,0]
	xval, yval = [], []
	N = len(points)
	#print N
	
	# Mean point of segment
	for a in range(int(N)):
		sumx += points[a][0]
		sumy += points[a][1]
		xval.append(points[a][0])
		yval.append(points[a][1])
	
	mean_point = [sumx / N, sumy / N]
	#print mean_point
	
	# Max and min values
	maxx = max(xval)
	minx = min(xval)
	maxy = max(yval)
	miny = min(yval)
	#print maxx, minx, maxy, miny
	
	# Initial and endpoints
	# Taking max and min values to set the length of the segment
	partial_segmentx = (maxx - minx) / 2
	partial_segmenty = (maxy - miny) / 2
	
	# Loading normalized angle values (0 - 255)
	angles_vals = angles.load()
	
	# Converting to its "orthogonal vector" by adding 64 (90 degrees)
	angle = (angles_vals[mean_point[0], mean_point[1]]) + 64
	if angle > 255:
		angle = angle - 255
	#print angle
	
	# Decision rules for the initial and end points of each segment.
	# If the angle is in the first and third quadrant the partial
	# segments are added or taken away to the initial and end points
	# respectively. If not, the add and subtract are mixed.
	if (angle >= 0 and angle <= 63) or \
	(angle >= 128 and angle <= 191):
		initial = (int(mean_point[0] + partial_segmentx), 
				   int(mean_point[1] + partial_segmenty))
		end = (int(mean_point[0] - partial_segmentx), 
		       int(mean_point[1] - partial_segmenty))
	else:
		initial = (int(mean_point[0] + partial_segmentx), 
				   int(mean_point[1] - partial_segmenty))
		end = (int(mean_point[0] - partial_segmentx), 
		       int(mean_point[1] + partial_segmenty))

  
	return initial, end

	
# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'figures.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	objects, segment, angles_norm, objs_data = object_detection(img,pixels)
	#print segment
	
	# Numpy array to store fitted lines
	width, height = objects.size
	lines = np.zeros((height,width,3), np.uint8)
	
	# Taking all segments and running line fitting
	for x in range(len(segment)):
		for y in range(len(segment[x])):
			segment_points = segment[x][y]
			if len(segment_points) > 10 and objs_data[x]._sides != 0:
				inipoint, endpoint = linefitting(segment_points, angles_norm)
				# Drawing fitted lines into lines array 
				cv2.line(lines, inipoint, endpoint,(0,255,255),1)
	
	# Showing results
	objects.show()
	cv2.imshow('image',lines)
	cv2.waitKey(0)
	cv2.destroyAllWindows()