from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
#from edge_detection import edge_detection
from object_detection_hw2 import object_detection
from PIL import Image
from PIL import ImageFont # Use fonts
from PIL import ImageDraw # Draw texts
import math
import numpy as np
import time # to use time.sleep('time in seconds')
import os # to construct a path relative to this script
#import matplotlib.pyplot as plt

def linefitting(points):
	# Initializing variables
	sumx, sumy, sumxx, sumyy, sumxy = 0.0, 0.0, 0.0, 0.0, 0.0
	alpha, beta, gamma = 0.0, 0.0, 0.0

	# Calculating sums from edge pixels:
	# Sum(x), Sum(y), Sum(x^2), Sum(y^2), Sum(x*y)
	N = float(len(points))
	for a in range(int(N)):
		sumx += float(points[a][0])
		sumy += float(points[a][1])
		sumxx += (sumx * sumx)
		sumyy += (sumy * sumy)
		sumxy += (sumx * sumy)
	print sumx, sumy, sumxx, sumyy, sumxy
	# Calculating alpha, beta and gamma
	alpha = sumxx - (pow(sumx,2) / N)
	beta = sumxy - ((sumx * sumy) / N)
	gamma = sumyy - (pow(sumy,2) / N)
	print alpha, beta, gamma

# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'figures.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	objects, segment = object_detection(img,pixels)
	#print segment
	
	for x in range(len(segment)):
		#print 'Object %d' % x
		for y in range(len(segment[x])):
			segment_points = segment[x][y]
			if len(segment_points) > 10:
				linefitting(segment_points)
			#print 'Segment %d' % y
			#print len(segment[x][y])
			#for z in range(len(segment[x][y])):
			#	print 'Points %d' % z
	
	#img = linefitting(segment)
	
	objects.show()