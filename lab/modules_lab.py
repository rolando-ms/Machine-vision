#**********************
# RGB to GS module
#**********************
# This module takes the data of an RGB image and converts it to gray 
# scale using GIMP's luminosity method according to: 
# http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/

def rgb_to_gs(original, new, imheight, imwidth):
	for y in range(imheight):
		for x in range(imwidth):
			new[x,y] = ((original[x,y][0] * 0.21) +
			(original[x,y][1] * 0.72) + (original[x,y][2] * 0.07))
			
	return new
	

#**********************
# Mask module
#**********************
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
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])
			# First row and any column in between
			elif ycoordinate == 0 and xcoordinate > 0 and xcoordinate < imwidth and b >= 0 and (xcoordinate + a) < imwidth:	
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])
			# First row and last column
			elif ycoordinate == 0 and xcoordinate == imwidth and a <= 0 and b >= 0:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])
			# Any row in between and first column
			elif ycoordinate > 0 and ycoordinate < imheight and xcoordinate == 0 and a >= 0 and (ycoordinate + b) < imheight:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])		
			# Any row in between any column in between
			elif ycoordinate > 0 and ycoordinate < imheight and xcoordinate > 0 and xcoordinate < imwidth and (xcoordinate + a) < imwidth and (ycoordinate + b) < imheight:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])	
			# Any row in between and last column
			elif ycoordinate > 0 and ycoordinate < imheight and xcoordinate == imwidth and a <= 0:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])
			# Last row and first column
			elif ycoordinate == imheight and xcoordinate == 0 and a >= 0 and b <= 0:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])	
			# Last row and any column in between
			elif ycoordinate == imheight and xcoordinate > 0 and xcoordinate <= imwidth and b <= 0 and (xcoordinate + a) < imwidth:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])
			# Last row and last column
			elif ycoordinate == imheight-1 and xcoordinate == imwidth-1 and a <= 0 and b <= 0:
				x_component += (image[xcoordinate+a,ycoordinate+b] * maskx[a+1,b+1])
				y_component += (image[xcoordinate+a,ycoordinate+b] * masky[a+1,b+1])
				
	return(x_component, y_component)