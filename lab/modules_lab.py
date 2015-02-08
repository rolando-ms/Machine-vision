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
			print 'x = %d , y = %d' %(x,y)
			new[x,y] = ((original[x,y][0] * 0.21) +
			(original[x,y][1] * 0.72) + (original[x,y][2] * 0.07))
			
	return new