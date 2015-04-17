from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
from object_detection_hw2 import object_detection
from PIL import Image
import math
import numpy as np
import cv2 # Open cv library
from random import randint

#---------------------
# Curve detection module
#---------------------
# This module takes lists of points and then calculates the rho to 
# get the line equation of the gradient angles. Then it votes and
# picks the most voted pixel as center.

def curve_detection(points, angles_rad, object):
	N = len(points)
	#angles_rad = angles_rad.load()
	width, height = angles_rad.shape
	#angles_new = Image.new('L', (width,height), "black")
	#angles_pix = angles_new.load()
	angles_pix = np.zeros((width,height), dtype = float)
	votes = np.zeros((width,height), np.uint8)
	
	for a in range(N/2):
		#selected = randint(0,N-1)
		selected = a
		angle_rad = angles_rad[points[selected][0], points[selected][1]]
		new_angle = angle_conversion(angle_rad)
		#print new_angle * (180/math.pi)
		
		# Calculating sine and cosine of the angle
		sine = math.sin(new_angle)
		if (sine > 0.0 and sine < 0.000001) or \
		(sine < 0.0 and sine > -0.000001):
			sine = 0.0
		#print 'sin(theta) = ' , sine #* (180/math.pi)
		
		cosine = math.cos(new_angle)
		if (cosine > 0.0 and cosine < 0.000001) or \
		(cosine < 0.0 and cosine > -0.000001):
			cosine = 0.0
		#print 'cos(theta) = ' , cosine #* (180/math.pi)
		
		x1 = float(points[selected][0])
		#print 'x1= ', x1
		y1 = float(points[selected][1])
		#print 'y1= ', y1
		
		# Normal line equation
		rho = int((x1 * cosine) + ((y1) * sine)) #float(height) -  ; you need to deduct height in order to have a common xy coordinate system equation, if not you get the programming image equation (inverted y)
		
		#print rho_aux, ' = x * cos(',angles_pix[points[a][0],points[a][1]],\
		#') + y * sin(',angles_pix[points[a][0],points[a][1]],')'
		#, line_angle
		voted = []
		# Voting
		if (new_angle > math.pi / 4 and new_angle < (3*math.pi) / 4) or\
		(new_angle > (math.pi / 4) + math.pi and new_angle < ((3*math.pi)/4)\
		+math.pi):
			lim1 = object._minx
			lim2 = object._maxx
			offset = int((lim2 - lim1) * 0.25)
			for x_coord in range(lim1 + offset,lim2 - offset):
				# Calculating x coordinates
				if sine == 0.0:
					y_coord = int(y1)
				else:
					y_coord = int((rho - x_coord * cosine) \
					/ sine)
				
				# +1 vote per new pair of coordinates
				if y_coord > 0 and y_coord < height:
					votes[x_coord,y_coord] += 1
					'''
					if x_coord == lim1:
						voted.append([x_coord,y_coord])
						votes[x_coord,y_coord] += 1
						#print 'votes + 1'
					else:
						for b in range(len(voted)):
							if [x_coord,y_coord] == voted[b]:
								break
							elif [x_coord,y_coord] != voted[b] and \
							b == lim2:
								voted.append([x_coord,y_coord])
								votes[x_coord,y_coord] += 1
								#print 'votes + 1'
					'''

		else:
			
			lim1 = object._miny
			lim2 = object._maxy
			offset = int((lim2 - lim1) * 0.25)
			for y_coord in range(lim1 + offset,lim2 - offset):
				# Calculating x coordinates
				if cosine == 0.0:
					x_coord = int(x1)
				else:
					x_coord = int((rho - y_coord * sine) \
					/ cosine)
				
				# +1 vote per new pair of coordinates
				if x_coord > 0 and x_coord < width:
					votes[x_coord,y_coord] += 1
					'''
					if y_coord == lim1:
						voted.append([x_coord,y_coord])
						votes[x_coord,y_coord] += 1
						#print 'votes + 1'
					else:
						for b in range(len(voted)):
							if [x_coord,y_coord] == voted[b]:
								break
							elif [x_coord,y_coord] != voted[b] and \
							b == lim2:
								voted.append([x_coord,y_coord])
								votes[x_coord,y_coord] += 1
								#print 'votes + 1'
					'''
	# Taking most voted point
	max_val = 0
	max_point = [0,0]
	for d in range(height):
		for c in range(width):
			#print 'c = ', c , 'd = ', d
			#if votes[c,d] > 0:
			#	print 'x = ',c,'y = ', d , 'value = ',votes[c,d]
			if votes[c,d] > 0 and votes[c,d] > max_val:
				#print 'inside'
				max_point = [c,d]
				max_val = votes[c,d]
	print max_val
	
	# Printing votes
	for d in range(height):
		for c in range(width):
			if votes[c,d] > 0:
				votes[c,d] = votes[c,d] * 5
	
	cv2.imshow('voting',votes)
	cv2.waitKey(0)
	
	return max_point
		
	
def angle_conversion(angle):
	# Adding 2 * pi to negative values
	if angle < 0:
		angle = angle + 2.0 * math.pi
	
	# If the angle == 5 (0 degrees)
	if angle == 5:
		angle = 0.0
	
	# Adding pi/2 (90 degrees; orthogonal vector)
	#angle += (-math.pi / 2.0)
	#if angle < 0: #> (2 * math.pi)
	#	angle += (2 * math.pi)
	
	# Angle + 180 == Angle
	#if angle > math.pi:
	#	angle += (-math.pi)
	
	conv_angle = angle
	return conv_angle

# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'figures.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	objects, segment, angles_norm, objs_data, angle_rads = object_detection(img,pixels)
	
	#print segment[0]
	
	# Transforming PIL image to opencv image
	img2 = Image.open(imgspath + name).convert('RGB')
	circles_rgb = np.array(img2)
	circles = circles_rgb[:,:,::-1].copy()
	
	width, height = objects.size

	z = 0
	# Taking all segments and running line fitting
	for x in range(len(segment)):
		#print 'Circle equation of object ', x
		#print objs_data[x]._minx, objs_data[x]._maxx
		#print objs_data[x]._miny, objs_data[x]._maxy
		for y in range(len(segment[x])):
			segment_points = segment[x][y]
			if len(segment_points) > 10 and (objs_data[x]._sides < 3 \
			or objs_data[x]._sides > 8):
				print 'circle'
				# Radius
				side1 = objs_data[x]._maxx - objs_data[x]._minx
				side2 = objs_data[x]._maxy - objs_data[x]._miny
				r = ((side1 + side2) / 2) / 2
				if abs(side1 - side2) < 0.1*side1:
					center_point = curve_detection(segment_points, \
					angle_rads, objs_data[x])
					
					# Drawing fitted lines into lines array
					center = tuple(center_point)
					cv2.circle(circles, center, r,(z,z,255),1)
		z += 40

	# Showing results
	objects.show()
	cv2.imshow('image',circles)
	cv2.waitKey(0)
	cv2.destroyAllWindows()