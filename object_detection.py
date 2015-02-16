from lab import modules_lab as modlab # Here I have my lab modules
from lecture import modules_lecture as modlec # Here I have my lecture modules
from edge_detection import edge_detection
from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('figures.png')
pixels = img.load()

magnitude, angle, edge = edge_detection(img, pixels)

edge.show()