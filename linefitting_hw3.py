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
import cv2 # Open cv library
#import matplotlib.pyplot as plt

def linefitting(points, imwidth, imheight):

	sumx, sumy, N, initial, end = 0.0, 0.0, 0.0, 0.0, 0.0
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
	print mean_point
	#return mean_point
	
	# Max and min values
	maxx = max(xval)
	minx = min(xval)
	maxy = max(yval)
	miny = min(yval)
	#print maxx, minx, maxy, miny
	
	# Initial and endpoints
	partial_segmentx = (maxx - minx) / 2
	partial_segmenty = (maxy - miny) / 2
	
	initial = (int(mean_point[0] + partial_segmentx), 
			   int(mean_point[1] + partial_segmenty))
	end = (int(mean_point[0] - partial_segmentx), 
		   int(mean_point[1] - partial_segmenty))
		   
	return initial, end
	
	'''
	#----------------------
	# Total Least Squares
	#----------------------
	# Initializing variables
	sumx, sumy, sumxx, sumyy, sumxy = 0.0, 0.0, 0.0, 0.0, 0.0
	alpha, beta, gamma = 0.0, 0.0, 0.0
	sum, c = 0.0, 0.0

	# Calculating sums from edge pixels:
	# Sum(x), Sum(y), Sum(x^2), Sum(y^2), Sum(x*y)
	N = float(len(points))
	for a in range(int(N)):
		sumx += float(points[a][0])
		sumy += float(imheight - points[a][1])
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
	# eigenvalue and the corresponding eigenvector. Eigenvector = norm
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
		sum += eigvec[0] * points[a][0] + eigvec[1] * points[a][1]
		
	c = -(sum / N)
	#print 'C value:'
	#print c
	
	# A point in the line
	point = -c * eigvec
	print point
	
	# Orthogonal vector
	ortho = np.array([[eigvec[1]],[-eigvec[0]]])
	
	# Tau values
	taus = []
	for a in range(int(N)):
		# Dot product between points and normal
		taus.append((points[a][0] * eigvec[0]) + (points[a][1] + eigvec[1]))
	
	#print taus
	# Max and min taus
	taumin = min(taus)
	taumax = max(taus)
	
	# Initial and end points of a segment
	#print 'ortho[0]'
	#print ortho[0]
	#print 'ortho[1]'
	#print ortho[1]
	initial = (point[0] + taumin * ortho[0], point[1] + taumin * ortho[1])
	end = (point[0] + taumax * ortho[0], point[1] + taumax * ortho[1])
	
	#return initial, end
	'''

# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'triangle.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	objects, segment = object_detection(img,pixels)
	#print segment
	
	# Numpy array
	width, height = objects.size
	img2 = np.zeros((height,width,3), np.uint8)
	
	for x in range(len(segment)):
		#print 'Object %d' % x
		for y in range(len(segment[x])):
			segment_points = segment[x][y]
			if len(segment_points) > 10:
				#linefitting(segment_points, width, height)
				inipoint, endpoint = linefitting(segment_points, width, height)
				cv2.line(img2, inipoint, endpoint,(0,255,255),1)
	
	#img = linefitting(segment)
	
	objects.show()
	cv2.imshow('image',img2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()