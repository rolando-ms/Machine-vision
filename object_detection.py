from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
from edge_detection import edge_detection
from PIL import Image
import math
import numpy as np
#import matplotlib.pyplot as plt

img = Image.open('figures.png')
pixels = img.load()

edge = Image.open('edge.png')
edge_pix = edge.load()

width, height = img.size

im2 = Image.new('RGB', (width,height), "black")
pixels2 = im2.load()

#magnitude, angle, edge = edge_detection(img, pixels)
#edge.show()
#edge_pix = edge.load()
#edge.save('edge.png')

# Getting background(BG) color according to the max number of pixels
colors = []
quantity = []
for y in range(height):
	for x in range(width):
		if len(colors) == 0:
			colors.append(pixels[x,y])
			quantity.append(1)
		else:
			for z in range(len(colors)):
				if pixels[x,y] == colors[z]:
					quantity[z] += 1
					break
				elif pixels[x,y] != colors[z] and \
					z == len(colors) - 1:
						colors.append(pixels[x,y])
						quantity.append(1)

for x in range(len(colors)):
	if quantity[x] == max(quantity):
		BG = colors[x]
		quantity = []	# Deleting data
		colors = []		# Deleting data
		break


objects = [] # [[(color),(minx,maxx,miny,maxy), # of pixels, cumulative x, cumulative y]]
edge_labels = []
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
		exists = 0
		dfs = 0
		current_color = 0
		#print pixels[x,y], x , y
		#first = 0
		while len(stack) > 0:

			if edge_pix[x,y] == 255 and labels_edge[x,y] == 0:
				edge_labels.append([0,0,[x,x,y,y]]) #(label, #pixels)
				dfs = 1
				label2 += 1
				c, d = x, y
				while dfs == 1 and len(stack) > 0:
					#print len(edge_labels)
					#remaining = 0
					labels_edge[c, d] = label2
					edge_labels[label2 - 1][0] = label2
					edge_labels[label2 - 1][1] += 1
					#edge_labels[label - 1][3] = objects[label - 1][3] + c
					#edge_labels[label - 1][4] = objects[label - 1][4] + d
				
					# min and max
					if c < edge_labels[label2 - 1][2][0]:
						edge_labels[label2 - 1][2][0] = c
					if c > edge_labels[label2 - 1][2][1]:
						edge_labels[label2 - 1][2][1] = c
					if d < edge_labels[label2 - 1][2][2]:
						edge_labels[label2 - 1][2][2] = d
					if d > edge_labels[label2 - 1][2][3]:
						edge_labels[label2 - 1][2][3] = d
				
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
								label2 != labels_edge[c + a, d + b] and \
								edge_pix[c + a, d + b] == 255: 
									remaining += 1 # pixels[c + a, d + b] == objects[label-1][0]
									c_aux, d_aux = c + a, d + b
									a_aux, b_aux = a, b
									#print remaining, pixels[c_aux,d_aux], objects[label-1][0]
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
			else:
				if len(objects) == 0:
					objects.append([pixels[x,y],[x,x,y,y],0,x,y])
					c, d = x, y
					dfs = 1
					label += 1
				elif labels[x,y] != label and edge_pix[x,y] != 255 and \
					labels[x,y] == 0:
					objects.append([pixels[x,y],[x,x,y,y],0,x,y])
					c, d = x, y
					dfs = 1
					label += 1
					#exists = 1
					#break
				else:
					break
			
		
				#print z_aux
				#print stack
				#print label
				#print objects
				while dfs == 1 and len(stack) > 0:
					labels[c, d] = label
					objects[label - 1][2] += 1
					objects[label - 1][3] = objects[label - 1][3] + c
					objects[label - 1][4] = objects[label - 1][4] + d
				
					# min and max
					if c < objects[label - 1][1][0]:
						objects[label - 1][1][0] = c
					if c > objects[label - 1][1][1]:
						objects[label - 1][1][1] = c
					if d < objects[label - 1][1][2]:
						objects[label - 1][1][2] = d
					if d > objects[label - 1][1][3]:
						objects[label - 1][1][3] = d
				
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
								pixels[c + a, d + b] == objects[label-1][0]: 
									remaining += 1 #
									c_aux, d_aux = c + a, d + b
									a_aux, b_aux = a, b
									#print remaining, pixels[c_aux,d_aux], objects[label-1][0]
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
					
'''
for c in range(2):
	for y in range(height):
		for x in range(width):
			found = 0
			if edge_pix[x,y] == 255 and labels[x,y] == 0:
				for a in range(-4,5):
					for b in range(-4,5):
						if pixels[x+a,y+b] != BG:
							labels[x,y] = labels[x+a,y+b]
							found = 1
							break
					if found == 1:
						break
'''

# Printing objects
for y in range(height):
	for x in range(width):
		#for z in range(len(objects)):
		pixels2[x,y] =((labels[x,y]-1)*30,
						(labels[x,y]-1)*15,
						(labels[x,y]-1)*15)
		if edge_pix[x,y] == 255 and \
		labels[x,y] > 1:
			pixels2[x,y] == (255,0,0)
		#elif edge_pix[x,y] == 255:
		#	pixels2[x,y] = (255,255,255)
		#print 'select'
		#print pixels[x,y]
		#break

# Printing centers of mass
for x in range(len(objects)):
	average_x, average_y = 0, 0
	cumulative_x = objects[x][3]
	cumulative_y = objects[x][4]
	total_pix = objects[x][2]
	average_x = cumulative_x / total_pix
	average_y = cumulative_y / total_pix
	#minx = objects[x][1][0] 
	#maxx = objects[x][1][1]
	#miny = objects[x][1][2] 
	#maxy = objects[x][1][3]
	#average_x = ((maxx - minx) / 2) + minx 
	#average_y = ((maxy - miny) / 2) + miny 
	#print minx, maxx, miny, maxy
	#print average_x, average_y
	pixels2[int(average_x), int(average_y)] = (0,255,0)

edgepix, edgelabel = 0, 0
for y in range(height):
	for x in range(width):
		if edge_pix[x,y] == 255:
			edgepix += 1
			if labels_edge[x,y] == 0:
				edgelabel += 1
	
print len(edge_labels)
print edgepix, edgelabel
img.show()
im2.show()
