#**********************
# RGB to GS function
#**********************
# This module takes the data of an RGB image and converts it to gray scale
# using GIMP's luminosity method according to: 
# http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/

def rgb_to_gs(original, new, imheight, imwidth):
	#data1 = pixels from original image, data 2 = pixels of new image
	for y in range(imheight):
		for x in range(imwidth):
			new[y,x] = ((original[y,x][0] * 0.21) +
			(original[y,x][1] * 0.72) + (original[y,x][2] * 0.07))
			
	return new