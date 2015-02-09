from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

# Opening target image
img = Image.open('circles_mini.png')
pixels = img.load()

# Saving resolution into variables
width, height = img.size

# Creating new GS images to store new pixels values in them
img2 = Image.new('L', (width,height), "black")
pixels2 = img2.load()

img3 = Image.new('L', (width,height), 'black')
pixels3 = img3.load()

# Creating result image
result = img
resultpix = result.load()

# Converting from RGB to GS
modlab.rgb_to_gs(pixels, pixels2, height, width)
#img2.show()

# Using sobel masks that minimizes angle errors according to:
# "Procesamiento digital de imagenes con MATLAB y Simulink"
# ISBN: 978-607-707-030-6
sobelx = np.array([[-3.0,0.0,3.0]
				,[-10.0,0.0,10.0]
				,[-3.0,0.0,3.0]])
sobely = np.array([[-3.0,-10.0,-3.0]
					,[0.0,0.0,0.0]
					,[3.0,10.0,3.0]])

# Creating zeros matrices to store values
magnitudes = np.zeros((width,height), dtype = float)
angles = np.zeros((width,height), dtype = float)

for y in range(height): # Rows
	for x in range(width):	# Columns
		
		# Discrete convolution to a pixel
		filterx, filtery = modlec.apply_edge_mask(pixels2, height, 
		width, y, x, sobelx, sobely)
						
		# Calculating magnitude with euclidean distance
		magnitudes[x,y] = modlec.euclidean_dist(filterx, filtery)
		
		# Calculating angle from components
		angles[x,y] = math.atan2(filtery, filterx)
		
		# Saving min and max magnitude values
		if x == 0 and y == 0:
			min = magnitudes[x,y]
			max = magnitudes[x,y]
		else:
			if magnitudes[x,y] < min:
				min = magnitudes[x,y]
			
			if magnitudes[x,y] > max:
				max = magnitudes[x,y]
				

# Creating list for histogram
histogram = []
bins = 50.0
for x in range(int(bins)):
	# Storing bins and initializing counters ==>(bins, counters)
	if x == bins - 1:
		histogram.append([255, 0])
	else:
		histogram.append([(255 / bins)*(x + 1), 0])

# Normalizing magnitudes and counting the corresponding pixels
max_hist = 0
max2_hist = 0
for x in range(height):
	for y in range(width):
		pixels3[y,x] = (magnitudes[y,x] - min) * (255 / max)
		magnitudes[y,x] = pixels3[y,x]
		for z in range(int(bins)):
			if magnitudes[y,x] <= histogram[z][0]:
				histogram[z][1] += 1
				if histogram[z][1] > max_hist:
					max_hist = histogram[z][1]
				break

# Getting the second maximum value of bins			
for z in range(int(bins)):
	if histogram[z][1] > max2_hist and histogram[z][1] < max_hist:
		max2_hist = histogram[z][1]

img3.show()
#print histogram , max_hist , max2_hist

# Printing pixels into result image
for y in range(height):
	for x in range(width):
		for z in range(int(bins)):
			if max_hist > ((height * width) * 0.7):
				if magnitudes[x,y] >= histogram[z][0] and histogram[z][1] < (max2_hist * 0.20):
					resultpix[x,y] = (255, 255, 0)
					break
			else:
				if histogram[z][1] < (max_hist * 0.20):
					if magnitudes[x,y] >= histogram[z][0]:
						#print histogram[z][1], max_hist*0.1
						resultpix[x,y] = (0, 255, 255)
						break


result.show()

'''
# Plotting histogram
values = np.zeros(1,int)

for x in range(height):	#Rows
	for y in range(width):	#Columns
		values = np.insert(values,0,magnitudes[y,x])
		

n, bins, patches = plt.hist(values, 50, facecolor = 'g')

plt.show()
'''


