import math

#************************
# Apply edge mask module
#************************
# This module applies an edge mask to a given image data and returns the 
# result of a certain pixel. This module must be located inside a double
# for loop to in order to be applied to all pixels.It takes the 
# boundaries into account.

def apply_edge_mask(image, imheight, imwidth, ycoordinate, xcoordinate,
maskx, masky):
	begin, end = -1, 2 # Initializing mask limits
	x_component = 0.0
	y_component = 0.0
		
	for a in range(begin, end):
		for b in range(begin, end):
			# First row and first column
			if ycoordinate == 0 and xcoordinate == 0 and a >= 0 and b >= 0:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])
			# First row and any column in between
			elif ycoordinate == 0 and xcoordinate > 0 and xcoordinate < imwidth and b >= 0 and (xcoordinate + a) < imwidth:	
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])
			# First row and last column
			elif ycoordinate == 0 and xcoordinate == imwidth and a <= 0 and b >= 0:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])
			# Any row in between and first column
			elif ycoordinate > 0 and ycoordinate < imheight and xcoordinate == 0 and a >= 0 and (ycoordinate + b) < imheight:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])		
			# Any row in between any column in between
			elif ycoordinate > 0 and ycoordinate < imheight and xcoordinate > 0 and xcoordinate < imwidth and (xcoordinate + a) < imwidth and (ycoordinate + b) < imheight:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])	
			# Any row in between and last column
			elif ycoordinate > 0 and ycoordinate < imheight and xcoordinate == imwidth and a <= 0:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])
			# Last row and first column
			elif ycoordinate == imheight and xcoordinate == 0 and a >= 0 and b <= 0:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])	
			# Last row and any column in between
			elif ycoordinate == imheight and xcoordinate > 0 and xcoordinate <= imwidth and b <= 0 and (xcoordinate + a) < imwidth:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])
			# Last row and last column
			elif ycoordinate == imheight-1 and xcoordinate == imwidth-1 and a <= 0 and b <= 0:
				x_component += (image[xcoordinate + a,ycoordinate + b] * maskx[a + 1,b + 1])
				y_component += (image[xcoordinate + a,ycoordinate + b] * masky[a + 1,b + 1])
				
	return(x_component, y_component)
	
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
	#begin, end = -2, 3 # Initializing mask limits
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
	#print "row = %d , column = %d , begin_row = %d , begin_col = %d" %(row,column,begin_row,begin_col)
		
	for a in range(begin_row, end_row):
		for b in range(begin_col, end_column):
			#print xcoordinate, ycoordinate, a, b
			#print 'column/2 = %d , row/2 = %d' %(column/2 + a,row/2 + b)
			if (xcoordinate + a) >= 0 and (xcoordinate + a) < imwidth and (ycoordinate + b) >= 0 and (ycoordinate + b) < imheight:
				#print "mask = %d , number = %d" %(mask[a + (column / 2),b + (row / 2)], number)
				cumulativeR += (image[xcoordinate + a,ycoordinate + b][0] * mask[a + (column / 2),b + (row / 2)])
				cumulativeG += (image[xcoordinate + a,ycoordinate + b][1] * mask[a + (column / 2),b + (row / 2)])
				cumulativeB += (image[xcoordinate + a,ycoordinate + b][2] * mask[a + (column / 2),b + (row / 2)])
				# Quantity to normalize cumulative values.
				# It is the sum of all digits used in the convolution.
				number += mask[a + (column / 2),b + (row / 2)]
				#print "mask = %d , number = %d" %(mask[a + (column / 2),b + (row / 2)], number)
			
	cumulativeR = cumulativeR / number
	cumulativeG = cumulativeG / number
	cumulativeB = cumulativeB / number
	#print 'cumulativeR = %d, cumulativeG = %d, cumulativeB = %d' %(cumulativeR, cumulativeG, cumulativeB)
	return (cumulativeR, cumulativeG, cumulativeB)

#***********************************************
# Convolution to a Gray Scale image in one pixel
#***********************************************
# This module applies the discrete convolution to a given image data and 
# returns the result of a certain pixel. This module must be located 
# inside a double for loop to in order to be applied to all pixels.
# It takes the boundaries into account.	

def convolution_gs_onepixel(image, mask, xcoordinate, ycoordinate, imheight, imwidth):
	#begin, end = -2, 3 # Initializing mask limits
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
	#print "row = %d , column = %d , begin_row = %d , begin_col = %d" %(row,column,begin_row,begin_col)
		
	for a in range(begin_row, end_row):
		for b in range(begin_col, end_column):
			#print xcoordinate, ycoordinate, a, b
			#print 'column/2 = %d , row/2 = %d' %(column/2 + a,row/2 + b)
			if (xcoordinate + a) >= 0 and (xcoordinate + a) < imwidth and (ycoordinate + b) >= 0 and (ycoordinate + b) < imheight:
				#print "mask = %d , number = %d" %(mask[a + (column / 2),b + (row / 2)], number)
				cumulative += (image[xcoordinate + a,ycoordinate + b] * mask[a + (column / 2),b + (row / 2)])
				# Quantity to normalize cumulative values.
				# It is the sum of all digits used in the convolution.
				number += mask[a + (column / 2),b + (row / 2)]
				#print "mask = %d , number = %d" %(mask[a + (column / 2),b + (row / 2)], number)
			
	cumulative = cumulative / number
	#print 'cumulativeR = %d, cumulativeG = %d, cumulativeB = %d' %(cumulativeR, cumulativeG, cumulativeB)
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