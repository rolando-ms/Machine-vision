from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
from edge_detection import edge_detection
from PIL import Image
from PIL import ImageFont # Use fonts
from PIL import ImageDraw # Draw texts
import math
import numpy as np
import time # to use time.sleep('time in seconds')
import os # to construct a path relative to this script
#import matplotlib.pyplot as plt

class object_data:
	data = 'color, min_max, pix_number, cumulative_x, cumulative_y \
	center_mass'
	
	def __init__(self):
		#self.object = 'object %d' %number
		self._color = ()
		self._minx = 0
		self._miny = 0
		self._maxx = 0
		self._maxy = 0
		self._pix_number = 0
		self._cumulative_x = 0
		self._cumulative_y = 0
		self._center_mass = []
	
	def color(self, colour):
		self._color = colour
		
	def center_mass(self, centerx, centery):
		self._center_mass.append(centerx)
		self._center_mass.append(centery)
		
	def label(self, current_label):
		self._label = current_label
		
class edge_labels_data:
	data = 'color, min_max, pix_number, cumulative_x, cumulative_y \
	center_mass'
	
	def __init__(self):
		#self.object = 'object %d' %number
		self._label = 0
		self._minx = 0
		self._miny = 0
		self._maxx = 0
		self._maxy = 0
		self._pix_number = 0
		self._cumulative_x = 0
		self._cumulative_y = 0
		self._center_mass = []
	
	def label(self, current_label):
		self._label = current_label
		
	def center_mass(self, centerx, centery):
		self._center_mass.append(centerx)
		self._center_mass.append(centery)
		
def object_detection(original_obj, original_obj_pix):
	# Getting sizes of target image
	width, height = original_obj.size
	
	# Creating result image
	objs = Image.new('RGB', (width,height), "black")
	objs_pix = objs.load()
	
	# Calculating magnitudes and angles of gradients. Getting edges.
	magnitude, angle, edge = edge_detection(original_obj, original_obj_pix)
	#edge.show()
	edge_pix = edge.load()
	#edge.save('edge.png')
	
	# Getting background color and the number of pixels
	BG = modlec.bg_color(objs)

	# Initializing variables
	objects2, edge_labels2 = [], []
	labels = np.zeros((width,height), dtype = int)
	labels_edge = np.zeros((width,height), dtype = int) # Auxiliary matrix
	label, label2, counter = 0, 0, 0
	
	# Scanning image for DFS
	for y in range(height):
		for x in range(width):
			remaining = 0 # Resetting. (Variable of remaining neighbors for DFS)
			stack = [[0,0]] # Resetting. (List of pixel coordinates for DFS)
			dfs = 0 # Flag to initialize DFS. 0 = avoid, 1 = continue
			
			# DFS for contours
			while len(stack) > 0:

				if edge_pix[x,y] == 255 and labels_edge[x,y] == 0:
					# Saving object into edge_labels
					edge_labels2.append(edge_labels_data())
					
					# Initializing min and max values
					edge_labels2[label2]._minx = x
					edge_labels2[label2]._maxx = x
					edge_labels2[label2]._miny = y
					edge_labels2[label2]._maxy = y
					dfs = 1
					label2 += 1
					multiplier = 20 # label 2 multiplier. It is used to have a different label than the objects.
					c, d = x, y # Saving x and y values for DFS
					
					while dfs == 1 and len(stack) > 0:
						labels_edge[c, d] = label2 * multiplier # Labelling pixel
						edge_labels2[label2 - 1].label(label2 * multiplier)
						
						# Incrementing values
						edge_labels2[label2 - 1]._pix_number += 1
						edge_labels2[label2 - 1]._cumulative_x += c
						edge_labels2[label2 - 1]._cumulative_y += d

						# Refreshing min and max values
						if c < edge_labels2[label2 - 1]._minx:
							edge_labels2[label2 - 1]._minx = c
						if c > edge_labels2[label2 - 1]._maxx:
							edge_labels2[label2 - 1]._maxx = c
						if d < edge_labels2[label2 - 1]._miny:
							edge_labels2[label2 - 1]._miny = d
						if d > edge_labels2[label2 - 1]._maxy:
							edge_labels2[label2 - 1]._maxy = d
						
						# Analysing remaining neighbors
						for b in range(-1, 2):
							for a in range(-1, 2):
								if  c + a >= 0 and \
									c + a <= width - 1 and \
									d + b >= 0 and \
									d + b <= height - 1 and \
									label2 * multiplier != labels_edge[c + a, d + b] and \
									edge_pix[c + a, d + b] == 255: 
										remaining += 1
										c_aux, d_aux = c + a, d + b
										a_aux, b_aux = a, b
					
						if remaining > 1:
							stack.append([c + a_aux,d + b_aux])
							c, d = c_aux, d_aux
						elif remaining == 1:
							c, d = c_aux, d_aux
						else:
							c, d = stack.pop()
						remaining = 0
				
				# DFS for objects (colors)
				else:
					if len(objects2) == 0 or (labels[x,y] != label and \
					edge_pix[x,y] != 255 and labels[x,y] == 0):
						# Saving object into objects
						objects2.append(object_data())
						
						# Initializing color, min and max values
						objects2[label].color(original_obj_pix[x,y])
						objects2[label]._minx = x
						objects2[label]._maxx = x
						objects2[label]._miny = y
						objects2[label]._maxy = y
						c, d = x, y
						dfs = 1
						label += 1
					else:
						break

					while dfs == 1 and len(stack) > 0:
						labels[c, d] = label # Labelling pixel
						
						# Incrementing values
						objects2[label - 1]._pix_number += 1
						objects2[label - 1]._cumulative_x += c
						objects2[label - 1]._cumulative_y += d

						# Refreshing min and max values
						if c < objects2[label - 1]._minx:
							objects2[label - 1]._minx = c
						if c > objects2[label - 1]._maxx:
							objects2[label - 1]._maxx = c
						if d < objects2[label - 1]._miny:
							objects2[label - 1]._miny = d
						if d > objects2[label - 1]._maxy:
							objects2[label - 1]._maxy = d

						# Analysing remaining neighbors
						for b in range(-1, 2):
							for a in range(-1, 2):
								if  c + a >= 0 and \
									c + a <= width - 1 and \
									d + b >= 0 and \
									d + b <= height - 1 and \
									label != labels[c + a, d + b] and \
									edge_pix[c + a, d + b] != 255 and \
									original_obj_pix[c + a, d + b] == objects2[label-1]._color: 
										remaining += 1
										c_aux, d_aux = c + a, d + b
										a_aux, b_aux = a, b				
						if remaining > 1:
							stack.append([c + a_aux,d + b_aux])
							c, d = c_aux, d_aux
						elif remaining == 1:
							c, d = c_aux, d_aux
						else:
							c, d = stack.pop()
						remaining = 0

	# Printing objects
	for y in range(height):
		for x in range(width):
			# Printing object pixels
			objs_pix[x,y] =((labels[x,y]-1)*30,
							(labels[x,y]-1)*15,
							(labels[x,y]-1)*15)
			if edge_pix[x,y] == 255 and \
			labels[x,y] > 1:
				objs_pix[x,y] == (255,0,0)
				
			# Printing edge pixels
			if edge_pix[x,y] == 255:
				objs_pix[x,y] = (255,255,255)

	
	# Calculating center of mass of objects
	for x in range(len(objects2)):
		average_x, average_y = modlec.get_center_mass(objects2[x])
		objects2[x].center_mass(average_x, average_y)
		objs_pix[int(average_x), int(average_y)] = (0,255,0)

	# Calculating center of mass of contours
	for x in range(len(edge_labels2)):
		average_x, average_y = modlec.get_center_mass(edge_labels2[x])
		edge_labels2[x].center_mass(average_x, average_y)
		objs_pix[int(average_x), int(average_y)] = (255,0,0)

	# Popping background from objects
	for x in range(len(objects2)):
		if objects2[x]._color == BG[0]:
			objects2.pop(x)
			break

	# Pairing edges and objects	together	
	for x in range(len(objects2)):
		for y in range(len(edge_labels2)):
			x1 = objects2[x]._minx
			x2 = objects2[x]._maxx
			y1 = objects2[y]._miny
			y2 = objects2[y]._maxy
			if(x2 - x1) < width * 0.05 and \
			(y2 - y1) < height * 0.05:
				objects2[x].label(y) # Saving label into object
				break

	# Normalizing angles and storing into im3
	im3 = Image.new('L', (width,height), "black")
	pixels3 = im3.load()
	labels_img = Image.new('L',(width,height), 'black')
	labels_aux = labels_img.load()
	angle_max, angle_min = 0.0, 0.0
	for y in range(height):
		for x in range(width):
			# Angle 0 was substituted by 5
			if angle[x,y] == 5:
				pixels3[x,y] = (math.pi) * (255 / (2 * math.pi) + 0.01)
				labels_aux[x,y] = pixels3[x,y]
			elif angle[x,y] != 0:
				pixels3[x,y] = (angle[x,y] + math.pi) * (255 / (2 * math.pi) + 0.15)
				labels_aux[x,y] = pixels3[x,y]
	
	# Angles image
	#im3.show()
	#im3.save('angles.png')

	quadrants = 24 # Quadrants to analyse
	segments = [] # List to save object's segments
	counter = 0
	
	# DFS to get the segments and its pixels
	for y in range(height):
		for x in range(width):
			stack = [[0,0]]
			dfs = 0
			
			while len(stack) > 0:

				if edge_pix[x,y] == 255 and \
				labels_aux[x,y] != 10:
					# Appending lists to store the resulting quadrant pixels
					segments.append([])
					for e in range(quadrants):
						segments[counter].append([])
					
					dfs = 1
					c, d = x, y
					
					while dfs == 1 and len(stack) > 0:
						labels_aux[c, d] = 10
						multiplier = 1
						
						# Appending pixel in the corresponding quadrant list
						for e in range(len(segments[counter])):
							if pixels3[c,d] <= ((255 / quadrants) * multiplier):
								segments[counter][e].append((c,d))
								break
							if e == len(segments[counter]) - 1:
								segments[counter][e].append((c,d))
								break
							multiplier += 1
						
						# Analysing remaining neighbors
						for b in range(-1, 2):
							for a in range(-1, 2):
								if  c + a >= 0 and \
									c + a <= width - 1 and \
									d + b >= 0 and \
									d + b <= height - 1 and \
									labels_aux[c + a, d + b] != 10 and \
									edge_pix[c + a, d + b] == 255: 
										remaining += 1 # original_obj_pix[c + a, d + b] == objects[label-1][0]
										c_aux, d_aux = c + a, d + b
										a_aux, b_aux = a, b
					
						if remaining > 1:
							stack.append([c + a_aux,d + b_aux])
							c, d = c_aux, d_aux
						elif remaining == 1:
							c, d = c_aux, d_aux
						else:
							c, d = stack.pop()
						remaining = 0
					counter += 1
				else:
					break

	# Deleting false objects (length = 0)
	for x in range(len(segments)):
		number = len(segments[x]) - 1
		for y in range(len(segments[x])):
			if len(segments[x][number]) == 0:
				segments[x].pop(number)
				number += -1
			else:
				number += -1

	# Counting sides of each object. It must have more than 10 pixels
	# to be counted as a side. This counts the changes from "high" to 
	# "low".
	sides = []
	for x in range(len(segments)):
		sides.append(0)
		for y in range(len(segments[x])):
			if len(segments[x][y]) > 10 and \
			y == len(segments[x]) - 1:
				sides[x] += 1
			elif len(segments[x][y]) > 10 and \
			len(segments[x][y+1]) < 10:
				sides[x] += 1
				
	# Printing bounding boxes
	# sides < 3 ==> C (circle)
	# sides =3 ==> T3 (Triangle)
	# sides = 4 ==> P4 (Polygon)
	# sides = 5 ==> P5 (Popygon), etc

	draw = ImageDraw.Draw(objs)
	font = ImageFont.load_default()
	detected = [[(255,0,0),'C'],[(255,0,0),'C'],[(0,255,0),'T3'],
	[(0,0,255),'P4'],[(255,255,0),'P5'],[(255,0,255),'P6'],
	[(0,255,255),'P7']]
	for z in range(len(objects2)):
		number = sides[z] - 1
		for x in range(4):
			if x == 0:
				for y in range(edge_labels2[z]._miny, edge_labels2[z]._maxy):
					objs_pix[edge_labels2[z]._minx,y] = detected[number][0]
			if x == 1:
				for y in range(edge_labels2[z]._miny, edge_labels2[z]._maxy):
					objs_pix[edge_labels2[z]._maxx,y] = detected[number][0]
			if x == 2:
				for y in range(edge_labels2[z]._minx, edge_labels2[z]._maxx):
					objs_pix[y,edge_labels2[z]._miny] = detected[number][0]	
			else:
				for y in range(edge_labels2[z]._minx, edge_labels2[z]._maxx):
					objs_pix[y,edge_labels2[z]._maxy] = detected[number][0]
			draw.text((objects2[z]._center_mass),detected[number][1],detected[number][0],font=font)

	objs.show()
	return objs

# Main function
if __name__ == "__main__":
	
	imgspath = 'benchmark_imgs/'
	name = 'figures.png'
	img = Image.open(imgspath + name)
	pixels = img.load()
	
	detected = object_detection(img,pixels)
	detected.show