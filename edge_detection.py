from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

def edge_detection(original, original_pix):
	# Opening target image
	#original = Image.open('figures.png')
	#original_pix = original.load()

	# Saving resolution into variables
	width, height = original.size

	# Creating new GS images to store new pixels values in them
	gray = Image.new('L', (width,height), "black")
	gray_pix = gray.load()

	# Creating result image
	result = original
	resultpix = result.load()

	# Converting from RGB to GS
	modlab.rgb_to_gs(original_pix, gray_pix, height, width)
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
			filterx, filtery = modlec.edge_gs_one(gray_pix, x, y, height, 
			width, sobelx, sobely)
							
			# Calculating magnitude with euclidean distance
			magnitudes[x,y] = modlec.euclidean_dist(filterx, filtery)
		
			# Calculating angle from components
			angles[x,y] = math.atan2(filtery, filterx)
			#print angles[x,y]
			# Saving min and max magnitude values
			if x == 0 and y == 0:
				min = magnitudes[x,y]
				max = magnitudes[x,y]
			else:
				if magnitudes[x,y] < min:
					min = magnitudes[x,y]
					
				if magnitudes[x,y] > max:
					max = magnitudes[x,y]


	# Creating normalization image to store values
	normalized = Image.new('L', (width,height), 'black')
	normalized_pix = normalized.load()

	# Normalizing magnitudes
	magnitudes, normalized_pix = modlec.normalize_edge(magnitudes, normalized_pix, height, width, min, max)
	#normalized.show()

	# Creating histogram
	histo = modlec.create_histogram(256, gray_pix, height, width)
	#print histo

	# Creating bin histogram (If colors are not discriminative)
	histogram_bin = modlec.reduce_histogram(histo, height, width)
	#print histogram_bin

	# Creating edges image to store edges values
	edges = Image.new('L', (width,height), 'black')
	edges_pix = edges.load()

	# Choosing edges
	edges_pix = modlec.chose_edges(histogram_bin, magnitudes, edges_pix, height, width)	
	#edges.show()

	# Printing edges on result image
	for y in range(height):
		for x in range(width):
			if edges_pix[x,y] > 0:
				resultpix[x,y] = (255,255,0)
	#result.show()
	
	return magnitudes, angles, edges



