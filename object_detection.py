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
#edge.save('edge.png')

objects = [] # [[(color),(minx,maxx,miny,maxy), # of pixels, average x, average y]]
labels = np.zeros((width,height), dtype = int)
label = 1
counter = 0
z_aux = 0
for y in range(height):
	for x in range(width):
		remaining = 0
		stack = [[0,0]]
		exists = 0
		dfs = 0
		#first = 0
		while len(stack) > 0:
			# Checking for existent colors
			for z in range(len(objects)):
				if len(objects) == 0:
					objects[z] = [pixels[x,y],[x,x,y,y],1,0,0]
					exists = 1
				elif objects[z][0] == pixels[x,y]:
					exists = 1	# The color already exists
					break
				elif z == len(objects) - 1:
					exists = 0	# The color doesn't exists
				
				z_aux = z
			'''
			if exists == 1 and objects[z][2] == 0:
				objects[z] = [(0,0,0),[x,x,y,y],1,0,0]
				labels[x,y] = label
				label += 1
				'''
			if exists == 1 and labels[x, y] == 0: # Label N/A
				c, d = x, y
				dfs = 1
			elif exists == 1 and labels[x, y] > 0: # Labelled
				break
			else: #exists == 0
				objects.append([pixels[x, y], [x,x,y,y], 1, 0, 0])
			'''
			if exists == 1 and label[x,y] != z + 1:
				#exists = 0
				# Checking for existent label
				if label[x,y] > 0: 
					for b in range(-1, 1):
						for a in range(-1, 1):
							if	pixels[x + a, y + b] == objects[z][0] and \
								z + 1 != labels[x,y] and \
								x + a >= 0 and \
								x + a <= width - 1 and \
								y + b >= 0 and \
								y + b <= height - 1 and
								edge[x + a, y + b] != 255:
									remaining += 1
									c, d = x + a, y + b
						
					if remaining > 1:
						stack.append([x + a,y + b])
					elif remaining == 0:
						stack.pop()
					
				else:
					# Assigning label depending on current color
					label[x,y] = objects[z] + 1
			
			elif exists == 1 and label[x, y] == z + 1:
				break
			
			elif exists == 0:
				# Appending new color and it's data. Assigning label.
				objects.append([[pixels[x,y]], [x,x,y,y], 1,0,0])
				labels[x,y] = label
				label += 1
			'''
			#print z_aux
			#print stack
			while dfs == 1 and len(stack) > 0:
				labels[c, d] = z_aux + 1
				#print stack
				#counter += 1
				#print counter
				for b in range(-1, 2):
					for a in range(-1, 2):
						#print c , d , a , b
						if  c + a >= 0 and \
							c + a <= width - 1 and \
							d + b >= 0 and \
							d + b <= height - 1 and \
							z_aux + 1 != labels[c + a, d + b] and \
							edge_pix[c + a, d + b] != 255 and \
							pixels[c + a, d + b] == objects[z_aux][0]:
								remaining += 1
								c_aux, d_aux = c + a, d + b
								a_aux, b_aux = a, b
								#print remaining
				#print 'c = %d , d = %d' %(c, d)
				#print remaining				
				if remaining > 1:
					stack.append([c + a_aux,d + b_aux])
					c, d = c_aux, d_aux
				elif remaining == 1:
					c, d = c_aux, d_aux
				else:
					# remaining == 0:
					c, d = stack.pop()
				remaining = 0
			#first == 1
print objects
print len(objects)
'''
im3 = Image.new('L', (width,height), "black")
pixels3 = im3.load()
pixels3 = labels
'''
# Printing objects
for y in range(height):
	for x in range(width):
		#for z in range(len(objects)):
		pixels2[x,y] =((labels[x,y]-1)*25,(labels[x,y]-1)*15,(labels[x,y]-1)*15)
		if edge_pix[x,y] == 255:
			pixels2[x,y] = (255,255,255)
		#print 'select'
		#print pixels[x,y]
		#break

img.show()
im2.show()