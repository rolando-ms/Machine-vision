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
	sum, c = 0.0, 0.0

	# Calculating sums from edge pixels:
	# Sum(x), Sum(y), Sum(x^2), Sum(y^2), Sum(x*y)
	N = float(len(points))
	for a in range(int(N)):
		sumx += float(points[a][0])
		sumy += float(points[a][1])
		sumxx += (sumx * sumx)
		sumyy += (sumy * sumy)
		sumxy += (sumx * sumy)
	#print sumx, sumy, sumxx, sumyy, sumxy
	
	# Calculating alpha, beta and gamma
	alpha = sumxx - ((sumx * sumx) / N)
	beta = sumxy - ((sumx * sumy) / N)
	gamma = sumyy - ((sumy * sumy) / N)
	#print alpha, beta, gamma
	
	# Arranging matrix, calculating eigenvalues and choosing the smaller
	# eigenvalue and the corresponding eigenvector
	mat = np.array([[alpha,beta],
					[beta,gamma]])
	eigen_val_vec = np.linalg.eig(mat)
	#print eigen_val_vec
	#print eigen
	if eigen_val_vec[0][0] < eigen_val_vec[0][1]:
		eigval = eigen_val_vec[0][0]
		eigvec = eigen_val_vec[1][:,0]
	else:
		eigval = eigen_val_vec[0][1]
		eigvec = eigen_val_vec[1][:,1]
	
	# Calculating c from eigvec
	for a in range(int(N)):
		sum += eigvec[0] * points[a][0] + eigvec[1] * points[0][1]
		
	c = -(sum / N)
	
	print c

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