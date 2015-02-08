from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('coins.png')
pixels = img.load()

img2 = Image.new('L', (img.size[0],img.size[1]), "black")
pixels2 = img2.load()

img3 = Image.new('L', (img.size[0],img.size[1]), 'black')
pixels3 = img3.load()

# Color to gray
for x in range(img.size[1]): # Rows
	for y in range(img.size[0]): # Columns
		#print 'x = %d , y = %d' %(x,y)
		pixels2[y,x] = ((pixels[y,x][0] * 0.21) + 
		(pixels[y,x][1] * 0.72) + (pixels[y,x][2] * 0.07))

#im2.show()

# Applying masks
# Sobel
sobelx = np.array([[-3.0,0.0,3.0],[-10.0,0.0,10.0],[-3.0,0.0,3.0]])
sobely = np.array([[-3.0,-10.0,-3.0],[0.0,0.0,0.0],[3.0,10.0,3.0]])
begin, end = -1, 2
magnitudes = np.zeros((img.size[0],img.size[1]), dtype = float)
angles = np.zeros((img.size[0],img.size[1]), dtype = float)

for x in range(img2.size[1]): # Rows
	for y in range(img2.size[0]):	# Columns
		counter = 0
		filterx = 0.0
		filtery = 0.0
		
		for a in range(begin, end):
			for b in range(begin, end):
				# First row and first column
				if x == 0 and y == 0 and a >= 0 and b >= 0:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1
				# First row and any column in between
				elif x == 0 and y > 0 and y < img2.size[0] and b >= 0 and (y + a) < img2.size[0]:	
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1
				# First row and last column
				elif x == 0 and y == img2.size[0] and a <= 0 and b >= 0:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1
				# Any row in between and first column
				elif x > 0 and x < img2.size[1] and y == 0 and a >= 0 and (x + b) < img2.size[1]:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1		
				# Any row in between any column in between
				elif x > 0 and x < img2.size[1] and y > 0 and y < img.size[0] and (y + a) < img2.size[0] and (x + b) < img2.size[1]:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1	
				# Any row in between and last column
				elif x > 0 and x < img2.size[1] and y == img2.size[0] and a <= 0:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1
				# Last row and first column
				elif x == img2.size[1] and y == 0 and a >= 0 and b <= 0:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1		
				# Last row and any column in between
				elif x == img2.size[1] and y > 0 and y <= img.size[0] and b <= 0 and (y + a) < img2.size[0]:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1	
				# Last row and last column
				elif x == img2.size[1]-1 and y == img.size[0]-1 and a <= 0 and b <= 0:
					filterx += (pixels2[y+a,x+b] * sobelx[a+1,b+1])
					filtery += (pixels2[y+a,x+b] * sobely[a+1,b+1])
					counter += 1
						
		Xpow = pow(filterx, 2)
		Ypow = pow(filtery, 2)
		magnitudes[y,x] = math.sqrt(Xpow + Ypow)
		angles[y,x] = math.atan2(filtery, filterx)
		if x == 0 and y == 0:
			min = magnitudes[y,x]
			max = magnitudes[y,x]
		else:
			if magnitudes[y,x] < min:
				min = magnitudes[y,x]
			
			if magnitudes[y,x] > max:
				max = magnitudes[y,x]
				

# Creating list for histogram
histogram = []
bins = 50.0
for x in range(int(bins)):
	# Storing bins and initializing counters ==>(bins, counters)
	if x == bins - 1:
		histogram.append([255, 0])
	else:
		histogram.append([(255 / bins)*(x + 1), 0])

# Normalizing magnitudes and counting the corresponding pixels
max_hist = 0
max2_hist = 0
for x in range(img.size[1]):
	for y in range(img.size[0]):
		pixels3[y,x] = (magnitudes[y,x] - min) * (255 / max)
		magnitudes[y,x] = pixels3[y,x]
		for z in range(int(bins)):
			if magnitudes[y,x] <= histogram[z][0]:
				histogram[z][1] += 1
				if histogram[z][1] > max_hist:
					max_hist = histogram[z][1]
				break

# Getting the second maximum value of bins			
for z in range(int(bins)):
	if histogram[z][1] > max2_hist and histogram[z][1] < max_hist:
		max2_hist = histogram[z][1]

img3.show()
#print histogram , max_hist , max2_hist

# Histogram	
for x in range(img.size[1]):
	for y in range(img.size[0]):
		for z in range(int(bins)):
			if max_hist > ((img.size[1] * img.size[0]) * 0.7):
				if magnitudes[y,x] >= histogram[z][0] and histogram[z][1] < (max2_hist * 0.20):
					pixels[y,x] = (255, 255, 0)
					break
			else:
				if histogram[z][1] < (max_hist * 0.20):
					if magnitudes[y,x] >= histogram[z][0]:
						#print histogram[z][1], max_hist*0.1
						pixels[y,x] = (0, 255, 255)
						break


# Plotting histogram
values = np.zeros(1,int)

for x in range(img.size[1]):	#Rows
	for y in range(img.size[0]):	#Columns
		values = np.insert(values,0,magnitudes[y,x])
		

n, bins, patches = plt.hist(values, 50, facecolor = 'g')
#plt.show()	

'''
# Plotting edges
print 'Choose cut limit:'
limit = int(raw_input('> '))

for x in range(img.size[1]):
	for y in range(img.size[0]):
		if magnitudes[y,x] > limit:
			pixels[y,x] = (0,255,0)
			'''
img.show()
plt.show()