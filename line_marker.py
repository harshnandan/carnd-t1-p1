import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

from helper_fnc import *

# read image
image = mpimg.imread('./test_images/whiteCarLaneSwitch.jpg')

imshape = image.shape

height_img = imshape[0]
width_img = imshape[1]


print("Height-" + str(height_img) + "; Width-" + str(width_img))
# plt.imshow(image)
# plt.show()

# convert image to gray scale
gray = grayscale(image);
# plt.imshow(gray, cmap='gray')
# plt.show()

# perform gaussian blur before feeding to edge detection
kernel_size = 5 # should be odd number
blur = gaussian_blur(gray, kernel_size)

# perform canny edge detection
low_threshold = 20
high_threshold = 100
edges = canny(blur, low_threshold, high_threshold)
# plt.imshow(edges, cmap='gray')
# plt.show()

 
vertices = np.array([[(0,height_img),
                      (np.int32(width_img/2)-10, height_img*0.55),
                      (np.int32(width_img/2)+10, height_img*0.55), 
                      (width_img, height_img)]], 
                      dtype=np.int32)

masked_edges = region_of_interest(edges, vertices)
# plt.imshow(masked)
# plt.show()

# Define the Hough transform parameters
rho = 2 
theta = np.pi/180 
threshold = 80     
min_line_length = 20 
max_line_gap = 1    

# Run Hough on edge detected image
lines_image = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

# Create a "color" binary image to combine with line image
color_edges = np.dstack((edges, edges, edges)) 
# 
# # Draw the lines on the edge image
lines_edges = weighted_img(color_edges, lines_image, alpha=1.0, beta=1., gamma=0.)

# plt input image and lane marked image
plt.figure(figsize=(10,5))
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(lines_edges)
plt.show()



