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