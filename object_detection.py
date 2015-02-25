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
	'''	
	def minx(self, minX):
		self._minx = minX
		
	def maxx(self, maxX):
		self._maxx = maxX

	def miny(self, minY):
		self._miny = minY
		
	def maxy(self, maxY):
		self._maxy = maxY
	'''
	def pix_number(self, num_pix):
		self._pix_number += num_pix
		
	def cumulative_x(self, cumulativex):
		self._cumulative_x += cumulativex

	def cumulative_y(self, cumulativey):
		self._cumulative_y += cumulativey
		
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
	'''
	def minx(self, minX):
		self._minx = minX
		
	def maxx(self, maxX):
		self._maxx = maxX

	def miny(self, minY):
		self._miny = minY
		
	def maxy(self, maxY):
		self._maxy = maxY
	'''	
	def pix_number(self, num_pix):
		self._pix_number += num_pix
		
	def cumulative_x(self, cumulativex):
		self._cumulative_x += cumulativex

	def cumulative_y(self, cumulativey):
		self._cumulative_y += cumulativey
		
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

	#print object_data.data
	
	#objects = [] # [[(color),(minx,maxx,miny,maxy), # of pixels, cumulative x, cumulative y]]
	objects2 = []
	#edge_labels = []
	edge_labels2 = []
	labels = np.zeros((width,height), dtype = int)
	labels_edge = np.zeros((width,height), dtype = int)
	label = 0
	label2 = 0
	counter = 0
	#z = 0
	for y in range(height):
		for x in range(width):
			remaining = 0
			stack = [[0,0]]
			#exists = 0
			dfs = 0
			current_color = 0
			#print original_obj_pix[x,y], x , y
			#first = 0
			while len(stack) > 0:

				if edge_pix[x,y] == 255 and labels_edge[x,y] == 0:
					edge_labels2.append(edge_labels_data())
					edge_labels2[label2]._minx = x
					edge_labels2[label2]._maxx = x
					edge_labels2[label2]._miny = y
					edge_labels2[label2]._maxy = y
					dfs = 1
					label2 += 1
					multiplier = 20 # label 2 multiplier
					c, d = x, y
					while dfs == 1 and len(stack) > 0:
						labels_edge[c, d] = label2 * multiplier
						edge_labels2[label2 - 1].label(label2 * multiplier)
						edge_labels2[label2 - 1]._pix_number += 1
						edge_labels2[label2 - 1]._cumulative_x += c
						edge_labels2[label2 - 1]._cumulative_y += d
					
						# min and max
						if c < edge_labels2[label2 - 1]._minx:
							edge_labels2[label2 - 1]._minx = c
						if c > edge_labels2[label2 - 1]._maxx:
							edge_labels2[label2 - 1]._maxx = c
						if d < edge_labels2[label2 - 1]._miny:
							edge_labels2[label2 - 1]._miny = d
						if d > edge_labels2[label2 - 1]._maxy:
							edge_labels2[label2 - 1]._maxy = d
					
						for b in range(-1, 2):
							for a in range(-1, 2):
								if  c + a >= 0 and \
									c + a <= width - 1 and \
									d + b >= 0 and \
									d + b <= height - 1 and \
									label2 * multiplier != labels_edge[c + a, d + b] and \
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
				else:
					if len(objects2) == 0:
						objects2.append(object_data())
						num = original_obj_pix[x,y]
						objects2[0].color(num)
						objects2[0]._minx = x
						objects2[0]._maxx = x
						objects2[0]._miny = y
						objects2[0]._maxy = y
						c, d = x, y
						dfs = 1
						label += 1
					elif labels[x,y] != label and edge_pix[x,y] != 255 and \
						labels[x,y] == 0:
						objects2.append(object_data())
						objects2[label].color(original_obj_pix[x,y])
						objects2[label]._minx = x
						objects2[label]._maxx = x
						objects2[label]._miny = y
						objects2[label]._maxy = y
						c, d = x, y
						dfs = 1
						label += 1
						#exists = 1
						#break
					else:
						break

					while dfs == 1 and len(stack) > 0:
						labels[c, d] = label
						objects2[label - 1]._pix_number += 1
						objects2[label - 1]._cumulative_x += c
						objects2[label - 1]._cumulative_y += d
					
						# min and max
						if c < objects2[label - 1]._minx:
							objects2[label - 1]._minx = c
						if c > objects2[label - 1]._maxx:
							objects2[label - 1]._maxx = c
						if d < objects2[label - 1]._miny:
							objects2[label - 1]._miny = d
						if d > objects2[label - 1]._maxy:
							objects2[label - 1]._maxy = d
					
						#print len(stack)
						#counter += 1
						#print counter
						for b in range(-1, 2):
							for a in range(-1, 2):
								#print c , d , a , b
								if  c + a >= 0 and \
									c + a <= width - 1 and \
									d + b >= 0 and \
									d + b <= height - 1 and \
									label != labels[c + a, d + b] and \
									edge_pix[c + a, d + b] != 255 and \
									original_obj_pix[c + a, d + b] == objects2[label-1]._color: 
										remaining += 1 #
										c_aux, d_aux = c + a, d + b
										a_aux, b_aux = a, b
										#print remaining, original_obj_pix[c_aux,d_aux], objects[label-1][0]
										#print label
						#print 'c = %d , d = %d' %(c, d)
						#print remaining				
						if remaining > 1:
							stack.append([c + a_aux,d + b_aux])
							c, d = c_aux, d_aux
							#print 'stack = %d , %d' %(c + a_aux, d + b_aux)
						elif remaining == 1:
							c, d = c_aux, d_aux
						else:
							# remaining == 0:
							c, d = stack.pop()
							#print 'popping'
						remaining = 0

	# Printing objects
	for y in range(height):
		for x in range(width):
			#for z in range(len(objects)):
			objs_pix[x,y] =((labels[x,y]-1)*30,
							(labels[x,y]-1)*15,
							(labels[x,y]-1)*15)
			if edge_pix[x,y] == 255 and \
			labels[x,y] > 1:
				objs_pix[x,y] == (255,0,0)
			
			if edge_pix[x,y] == 255:
				objs_pix[x,y] = (255,255,255)
			#print 'select'
			#print pixels[x,y]
			#break

	# Printing centers of mass of objects
	for x in range(len(objects2)):
		average_x, average_y = 0, 0
		cumulative_x = objects2[x]._cumulative_x
		cumulative_y = objects2[x]._cumulative_y
		#print cumulative_x, cumulative_y
		total_pix = objects2[x]._pix_number
		average_x = cumulative_x / total_pix
		average_y = cumulative_y / total_pix
		objects2[x].center_mass(average_x, average_y)
		objs_pix[int(average_x), int(average_y)] = (0,255,0)
		
	# Printing centers of mass 2 (of contours)
	for x in range(len(edge_labels2)):
		average_x, average_y = 0, 0
		cumulative_x = edge_labels2[x]._cumulative_x
		cumulative_y = edge_labels2[x]._cumulative_y
		#print cumulative_x, cumulative_y
		total_pix = edge_labels2[x]._pix_number
		average_x = cumulative_x / total_pix
		average_y = cumulative_y / total_pix
		edge_labels2[x].center_mass(average_x, average_y)
		objs_pix[int(average_x), int(average_y)] = (255,0,0)

	# Popping background from objects
	for x in range(len(objects2)):
		if objects2[x]._color == BG[0]:
			#background = objects.pop(x)
			objects2.pop(x)
			break

	# Pairing edges and objects	together	
	for x in range(len(objects2)):
		for y in range(len(edge_labels2)):
			#found = 0
			x1 = objects2[x]._minx
			x2 = objects2[x]._maxx
			y1 = objects2[y]._miny
			y2 = objects2[y]._maxy
			#print x1, x2, y1, y2
			if(x2 - x1) < width * 0.05 and \
			abs(y2 - y1) < height * 0.05:
				#objects[x][6] = y
				objects2[x].label(y)
				#found = 1
				break



	#original_obj.show()
	#objs.show()
	#objs.save('objects.png')

	# Normalizing angles and storing into im3
	im3 = Image.new('L', (width,height), "black")
	pixels3 = im3.load()
	labels_img = Image.new('L',(width,height), 'black')
	labels_aux = labels_img.load()
	angle_max, angle_min = 0.0, 0.0
	for y in range(height):
		for x in range(width):
			if angle[x,y] == 5:
				pixels3[x,y] = (math.pi) * (255 / (2 * math.pi) + 0.01)
				labels_aux[x,y] = pixels3[x,y]
				#print pixels3[x,y]
			elif angle[x,y] != 0:
				pixels3[x,y] = (angle[x,y] + math.pi) * (255 / (2 * math.pi) + 0.15)
				labels_aux[x,y] = pixels3[x,y]
				#print pixels3[x,y]
			# Maximum and minimum angle values
			if angle[x,y] > angle_max and angle[x,y] != 5:
				angle_max = angle[x,y]
			if angle[x,y] < angle_min:
				angle_min = angle[x,y]
	#print angle_max, angle_min

	#im3.show()
	#im3.save('angles.png')


	#objects = [] # [[(color),(minx,maxx,miny,maxy), # of pixels, cumulative x, cumulative y]]
	#edge_labels = []
	#labels = np.zeros((width,height), dtype = int)
	#labels_edge = np.zeros((width,height), dtype = int)
	#segments = [] # edge_labels, segments
	#label = 0
	#label2 = 0
	quadrants = 24
	segments = []
	#labels_aux = pixels3
	counter = 0
	#multiplier = 0
	for y in range(height):
		for x in range(width):
			stack = [[0,0]]
			#print pixels3[x,y]
			#exists = 0
			dfs = 0
			#multiplier = 0
			while len(stack) > 0:

				if edge_pix[x,y] == 255 and \
				labels_aux[x,y] != 10:
					segments.append([])
					for e in range(quadrants):
						segments[counter].append([])
						
					#segments.append([])
					#segments[counter].append([pixels3[x, y],[]])
					#edge_labels.append([0,[x,x,y,y],0,0,0,(0,0)]) #(label,[minx,maxx,miny,maxy], #pixels,cumulative_x,cumulative_y,(center of mass xy))
					dfs = 1
					c, d = x, y
					
					while dfs == 1 and len(stack) > 0:
						labels_aux[c, d] = 10
						multiplier = 1
						for e in range(len(segments[counter])):
							if pixels3[c,d] <= ((255 / quadrants) * multiplier):
								segments[counter][e].append((c,d))
								#print multiplier
								#print segments[counter]
								#time.sleep(0.5)
								break
							if e == len(segments[counter]) - 1:
								segments[counter][e].append((c,d))
								break
							multiplier += 1
							
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
						#print len(stack)
					counter += 1
					#segments.append([])
				else:
					break

	# Deleting small segments and false objects
	for x in range(len(segments)):
		#print 'Object %d' % x
		number = len(segments[x]) - 1
		for y in range(len(segments[x])):
			#print len(segments[x][number])
			if len(segments[x][number]) == 0:
				segments[x].pop(number)
				number += -1
				#print 'Popping'
			else:
				number += -1

	# Counting sides of each object
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
	#print objects
	#print edge_labels
	#print sides
	draw = ImageDraw.Draw(objs)
	font = ImageFont.load_default()
	detected = [[(255,0,0),'C'],[(255,0,0),'C'],[(0,255,0),'T3'],[(0,0,255),'P4'],[(255,255,0),'P5'],[(255,0,255),'P6'],[(0,255,255),'P7']]
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