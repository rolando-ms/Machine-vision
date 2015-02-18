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
label = 0
counter = 0
#z = 0
for y in range(height):
	for x in range(width):
		remaining = 0
		stack = [[0,0]]
		exists = 0
		dfs = 0
		#print pixels[x,y], x , y
		#first = 0
		while len(stack) > 0:

			if len(objects) == 0:
				objects.append([pixels[x,y],[x,x,y,y],1,0,0])
				c, d = x, y
				dfs = 1
				label += 1
			elif labels[x,y] != label and edge_pix[x,y] != 255 and \
				labels[x,y] == 0:
				objects.append([pixels[x,y],[x,x,y,y],1,0,0])
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
								remaining += 1
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
				#if c == width - 1 and d == height - 1:
				#		break
				#if len(stack) == 0:
				#	break
			#first == 1
			'''
			if len(stack) == 0:
				print 'End DFS!!!!!!!!!'
				break
			'''
		
		#print x, y
		#print objects
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
		pixels2[x,y] =((labels[x,y]-1)*30,(labels[x,y]-1)*15,(labels[x,y]-1)*15)
		if edge_pix[x,y] == 255:
			pixels2[x,y] = (255,255,255)
		#print 'select'
		#print pixels[x,y]
		#break

img.show()
im2.show()