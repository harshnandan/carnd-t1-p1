import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

from helper_fnc import *

def lineMarkerFnc(image, line_state, line_uncertanity, figNumber=1, totalFigures=1, figSize=(10,5)):
    
    imshape = image.shape
    
    height_img = imshape[0]
    width_img = imshape[1]
#     print("Height-" + str(height_img) + "; Width-" + str(width_img))

    plt.imshow(image)
    plt.savefig( "./pipeline_steps/step_0_original.png", bbox_inches='tight', transparent="True", pad_inches=0)
#     plt.show()
    
    
    # convert image to gray scale
    gray = grayscale(image);
    plt.imshow(gray, cmap='gray')
    plt.savefig( "./pipeline_steps/step_1_grayScale.png", bbox_inches='tight', transparent="True", pad_inches=0)
#     plt.show()
    
    # perform gaussian blur before feeding to edge detection
    kernel_size = 5 # should be odd number
    blur = gaussian_blur(gray, kernel_size)
    plt.imshow(blur, cmap='gray')
    plt.savefig( "./pipeline_steps/step_2_blur.png", bbox_inches='tight', transparent="True", pad_inches=0)
    
    # perform canny edge detection
    low_threshold = 50
    high_threshold = 150
    edges = canny(blur, low_threshold, high_threshold)
    plt.imshow(edges, cmap='gray')
    plt.savefig( "./pipeline_steps/step_3_CannyEdge.png", bbox_inches='tight', transparent="True", pad_inches=0)
#     plt.show()

    vertices = np.array([[(0,height_img),
                          (np.int32(width_img/2)-10, height_img*0.57),
                          (np.int32(width_img/2)+10, height_img*0.57), 
                          (width_img, height_img)]], 
                          dtype=np.int32)
    
    masked_edges = region_of_interest(edges, vertices)
    plt.imshow(masked_edges, cmap='gray')
    plt.savefig( "./pipeline_steps/step_4_RegionInterest.png", bbox_inches='tight', transparent="True", pad_inches=0)
#     plt.show()
    
    # Define the Hough transform parameters
    rho = 2 
    theta = np.pi/180 
    threshold = 80
    min_line_length = 5 
    max_line_gap = 1    
    
    # Run Hough on edge detected image
    lines_image = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap, line_state, line_uncertanity)
    plt.imshow(lines_image['img'], cmap='gray')
    plt.savefig( "./pipeline_steps/step_5_Lines.png", bbox_inches='tight', transparent="True", pad_inches=0)
    
    # Create a "color" binary image to combine with line image
    color_edges = np.dstack((edges, edges, edges)) 
    # 
    # # Draw the lines on the edge image
    lines_edges = weighted_img(image, lines_image['img'], alpha=1.0, beta=1., gamma=0.)
    plt.imshow(lines_edges)
    plt.savefig( "./pipeline_steps/step_6_Superimposed.png", bbox_inches='tight', transparent="True", pad_inches=0)

    
#     # plt input image and lane marked image
#     plt.figure(figsize=figSize)
#     plt.subplot(121)
#     plt.imshow(image)
#     plt.subplot(122)
#     plt.imshow(lines_edges)
#     plt.show()
    
    return {'img':lines_edges, 'lines':lines_image['lines']}

if __name__ == '__main__':
    fileName = 'solidYellowCurve.jpg'
    image = mpimg.imread('test_images/' + fileName)
    
    line_state = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    line_state = line_state[..., np.newaxis]
    line_uncertanity = np.zeros((8,8))
    line_uncertanity[0] = 1
    line_uncertanity[1] = 1
    line_uncertanity[2] = 1000
    line_uncertanity[3] = 1000
    line_uncertanity[4] = 1
    line_uncertanity[5] = 1
    line_uncertanity[6] = 1000
    line_uncertanity[7] = 1000
    
    out_image = lineMarkerFnc(image, line_state, line_uncertanity)
    cv2.imwrite('./test_images_output/' + fileName, cv2.cvtColor(out_image['img'],cv2.COLOR_RGB2BGR))
    
