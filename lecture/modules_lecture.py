import math

#************************
# Apply edge mask module
#************************
# This module applies 2 edge masks to a given image data and returns the 
# result of a certain pixel. This module must be located inside a double
# for loop to in order to be applied to all pixels.It takes the 
# boundaries into account.
	
def edge_gs_one(image, xcoordinate, ycoordinate, imheight, imwidth, maskx, masky):
	# Initializing variables
	x_component, y_component = 0, 0
	
	# Assigning the size of the mask
	row = maskx.shape[0]
	column = maskx.shape[1]
	
	# Assigning ranges of for loops according to the size of the mask
	begin_row = (row/2) * -1
	begin_col = (column/2) * -1
	if (row % 2) == 0:	# If it is even
		end_row = row / 2
	else:				# If it is odd
		end_row = (row / 2) + 1
		
	if (column % 2) == 0:
		end_column = column / 2
	else:
		end_column = (column / 2) + 1
	
	# Convolution
	for a in range(begin_row, end_row):
		for b in range(begin_col, end_column):
			if (xcoordinate + a) >= 0 and (xcoordinate + a) < imwidth and (ycoordinate + b) >= 0 and (ycoordinate + b) < imheight:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + (column / 2),b + (row / 2)])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + (column / 2),b + (row / 2)])
			
	return (x_component, y_component)

	
#*****************************************
# Convolution to an RGB image in one pixel
#*****************************************
# This module applies the discrete convolution to a given image data and 
# returns the result of a certain pixel. This module must be located 
# inside a double for loop to in order to be applied to all pixels.
# It takes the boundaries into account.	

def convolution_rgb_onepixel(image, mask, xcoordinate, ycoordinate, imheight, imwidth):
	# Initializing variables
	cumulativeR, cumulativeG, cumulativeB, number = 0, 0, 0, 0
	
	# Assigning the size of the mask
	row = mask.shape[0]
	column = mask.shape[1]
	
	# Assigning ranges of for loops according to the size of the mask
	begin_row = (row/2) * -1
	begin_col = (column/2) * -1
	if (row % 2) == 0: # If it is even
		end_row = row / 2
	else:			   # If it is odd
		end_row = (row / 2) + 1
		
	if (column % 2) == 0:
		end_column = column / 2
	else:
		end_column = (column / 2) + 1
	
	# Convolution	
	for a in range(begin_row, end_row):
		for b in range(begin_col, end_column):
			if (xcoordinate + a) >= 0 and (xcoordinate + a) < imwidth and (ycoordinate + b) >= 0 and (ycoordinate + b) < imheight:
				cumulativeR += (image[xcoordinate + a,ycoordinate + b][0] * mask[a + (column / 2),b + (row / 2)])
				cumulativeG += (image[xcoordinate + a,ycoordinate + b][1] * mask[a + (column / 2),b + (row / 2)])
				cumulativeB += (image[xcoordinate + a,ycoordinate + b][2] * mask[a + (column / 2),b + (row / 2)])
				# Quantity to normalize cumulative values.
				# It is the sum of all digits used in the convolution.
				number += mask[a + (column / 2),b + (row / 2)]
			
	cumulativeR = cumulativeR / number
	cumulativeG = cumulativeG / number
	cumulativeB = cumulativeB / number
	return (cumulativeR, cumulativeG, cumulativeB)

#***********************************************
# Convolution to a Gray Scale image in one pixel
#***********************************************
# This module applies the discrete convolution to a given image data and 
# returns the result of a certain pixel. This module must be located 
# inside a double for loop to in order to be applied to all pixels.
# It takes the boundaries into account.	

def convolution_gs_onepixel(image, mask, xcoordinate, ycoordinate, imheight, imwidth):
	# Initializing variables
	cumulative, number = 0, 0
	
	# Assigning the size of the mask
	row = mask.shape[0]
	column = mask.shape[1]
	
	# Assigning ranges of for loops according to the size of the mask
	begin_row = (row/2) * -1
	begin_col = (column/2) * -1
	if (row % 2) == 0:	# If it is even
		end_row = row / 2
	else:				# If it is odd
		end_row = (row / 2) + 1
		
	if (column % 2) == 0:
		end_column = column / 2
	else:
		end_column = (column / 2) + 1
	
	# Convolution
	for a in range(begin_row, end_row):
		for b in range(begin_col, end_column):
			if (xcoordinate + a) >= 0 and (xcoordinate + a) < imwidth and (ycoordinate + b) >= 0 and (ycoordinate + b) < imheight:
				cumulative += (image[xcoordinate + a,ycoordinate + b] * mask[a + (column / 2),b + (row / 2)])
				# Quantity to normalize cumulative values.
				# It is the sum of all digits used in the convolution.
				number += mask[a + (column / 2),b + (row / 2)]
			
	cumulative = cumulative / number
	return (cumulative)

#***************************
# Euclidean distance module	
#***************************
# Given two int magnitudes, this module returns the euclidean distance
# from them.

def euclidean_dist(xval, yval):
	xpow = pow(xval, 2)
	ypow = pow(yval, 2)
	magnitude = math.sqrt(xpow + ypow)
	return magnitude
	
#**********************************
# Normalization of edge magnitudes
#**********************************
# Given an image and it's max and min values, this module returns an 
# image with normalized values (0-255)

def normalize_edge(magnitude, image_pix, imheight, imwidth, mini, maxi):
	#image = Image.new('L', (width,height), 'black')
	#image_pix = image.load()
	#imheight, imwidth = image.size[1], image.size[0]
	for y in range(imheight):
		for x in range(imwidth):
			image_pix[x,y] = (magnitude[x,y] - mini) * (255 / maxi)
			magnitude[x,y] = image_pix[x,y]
	
	return magnitude, image_pix
			
	
	
#******************
# Histogram module
#******************
# This module creates a histogram for a grey image and initializes 
# it's values.

def create_histogram(hist_len, image, imheight, imwidth):
	# Creating histogram
	histogram = [0] * hist_len
	
	# Incrementing histogram values reading pixel values
	for y in range(imheight):
		for x in range(imwidth):
			value = image[x,y]
			histogram[value] += 1 
	#print histogram
	
	return histogram

def reduce_histogram(histogram):
	# Initializing a routine to find zeros in the histogram and, if so,
	# joining pairs of values to create bins until no zero is found or
	# the histogram has a length of 2.
	
	reduce, exit = 0, 0
	while(exit == 0):
		# If histogram has a length of 2 ==> exit
		#(No more reductions allowed)
		if len(histogram) == 2:
			#exit == 1
			break
		# Looking for zeros
		for z in range(len(histogram)):
			#print z, len(histogram)
			if histogram[z] == 0:
				reduce = 1
				break
			if histogram[z] != 0 and z == len(histogram) - 1:
				exit = 1
		
		# Reducing histogram by pairing couples of values and popping
		if reduce == 1:
			reduce = 0; # Reduce variable reset
			a, b = 0, 1 # Initializing variables
			for w in range(len(histogram)):
				# Pairing couples
				if w < (len(histogram) / 2):
					histogram[w] = histogram[a] + histogram[b]
					a += 2
					b += 2
				# Popping values
				else:
					histogram.pop()
		
		#print histogram
		
	return histogram