#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 15:24
# @Author  : Wang Zixv
# @Site    : 
# @File    : get_line_hog.py.py
# @Software: PyCharm


import cv2
import numpy as np
import matplotlib.pyplot as plt


# Set the default figure size
plt.rcParams['figure.figsize'] = [17.0, 7.0]

# Load the image
image = cv2.imread('./images/triangle_tile.jpeg')

# Convert the original image to RGB
original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert the original image to gray scale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Print the shape of the original and gray scale images
print('The original image has shape: ', original_image.shape)
print('The gray scale image has shape: ', gray_image.shape)

# Display the images
plt.subplot(121)
plt.imshow(original_image)
plt.title('Original Image')
plt.subplot(122)
plt.imshow(gray_image, cmap='gray')
plt.title('Gray Scale Image')
plt.show()
