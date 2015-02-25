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
	
	

# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'figures.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	objects, segment = object_detection(img,pixels)
	#print segment
	
	for x in range(len(segment)):
		print 'Object %d' % x
		for y in range(len(segment[x])):
			print 'Segment %d' % y
			print len(segment[x][y])
			#for z in range(len(segment[x][y])):
			#	print 'Points %d' % z
	
	#img = linefitting(segment)
	
	objects.show()