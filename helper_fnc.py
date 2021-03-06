import math
import numpy as np
import cv2
import matplotlib.pyplot as plt

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, np.array(vertices, dtype=np.int32), ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, line_state, P, color=[0, 255, 255], thickness=5):

    
    slope_intercept = np.zeros((lines.shape[0], 2), dtype=np.float32)
    counter = 0
    countList = []
    # loop over all the lines detected by Hough transform 
    for line in lines:
        for x1,y1,x2,y2 in line:
            # cv2.line(img, (x1, y1), (x2, y2), color, thickness)
            # calculate slope of each line
            # avoid devide by zero condition
            if (x2==x1):
                m = 1000
            else:
                m = (y2-y1)/(x2-x1)
            b = y2 - m*x2
            
            # ignore lines which are almost horizontal
            # especially useful for the challenge video
            if np.abs(m) < 0.1:
                countList.append(counter)

            slope_intercept[counter, :] =  [m, b]
            counter += 1
    
    # delete rows corresponding to lines which are almost horizontal
    slope_intercept = np.delete(arr=slope_intercept, obj=countList, axis=0)
    
    # Conduct K mean clustering to find mean slope and intercept
    # for two lane markers
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(slope_intercept,2,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    
    # Flag to start kamlman filtering only in second iteration for videos
    # Kalman filter does not engage for static image
    second_run = False
    if (line_state[0,0]!=0 and line_state[4,0]!=0):
        second_run = True
    
    # if clustering finds only one class
    # assume it is the same as last state
    if (center.shape[1] == 1):
        m1 = line_state[0,0]
        b1 = line_state[1,0]
        m2 = line_state[4,0]
        b2 = line_state[5,0]
    else:
        if center[0, 0] < center[1, 0]:
            m1 = center[0, 0]
            b1 = center[0, 1]
            m2 = center[1, 0]
            b2 = center[1, 1]
        else:
            m1 = center[1, 0]
            b1 = center[1, 1]
            m2 = center[0, 0]
            b2 = center[0, 1]

    # apply kalman filtering from 2nd frame on
    if second_run:
        line_state, P = kalmanFilterFnc(line_state, P, np.array([m1, b1, m2, b2]).T)
        m1 = line_state[0, 0]
        b1 = line_state[1, 0]
        m2 = line_state[4, 0]
        b2 = line_state[5, 0]
    else:
        line_state = np.array([m1, b1, 0, 0, m2, b2, 0, 0]).T
        line_state = line_state[..., np.newaxis]
    
    # draw lines in region of interest
    y1av_1 = img.shape[0]
    x1av_1 = np.int32(1/m1*(y1av_1 - b1))
    
    y2av_1 = np.int32(0.6 * img.shape[0])
    x2av_1 = np.int32(1/m1*(y2av_1 - b1))
    
    cv2.line(img, (x1av_1, y1av_1), (x2av_1, y2av_1), [255, 0, 0], thickness)
    
    y1av_2 = img.shape[0]
    x1av_2 = np.int32(1/m2*(y1av_2 - b2))
    
    y2av_2 = np.int32(0.6 * img.shape[0])
    x2av_2 = np.int32(1/m2*(y2av_2 - b2))
    
    cv2.line(img, (x1av_2, y1av_2), (x2av_2, y2av_2), [255, 0, 0], thickness)

#     Some debug plotting code    
#     # Now separate the data, Note the flatten()
#     A = slope_intercept[label.ravel()==0]
#     B = slope_intercept[label.ravel()==1]
#            
#     # Plot the data
#     plt.scatter(A[:,0],A[:,1])
#     plt.scatter(B[:,0],B[:,1],c = 'r')
#     plt.scatter(center[:,0],center[:,1],s = 80,c = 'y', marker = 's')
#     plt.scatter([m1, m2], [b1, b2],s = 80,c = 'k', marker = 'x')
#     plt.xlabel('m'),plt.ylabel('b')
#     plt.savefig( "./pipeline_steps/step_7_Slope_intercept_KMean.png", bbox_inches='tight', transparent="True", pad_inches=0)
# #    plt.show()  

    return line_state, P
    
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap, line_state, line_uncertanity):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    smooth_line_parms, P = draw_lines(line_img, lines, line_state, line_uncertanity)
    return {'img':line_img, 'lines':[smooth_line_parms, P]}

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, alpha=0.8, beta=1., gamma=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, alpha, img, beta, gamma)

def kalmanFilterFnc(x, P, measurement):
    '''
    Parameters:
    x:             initial state
    P:             initial uncertainty convariance matrix
    measurement:   observed position (same shape as H*x)
    R:             measurement noise (same shape as H)
    F:             next state function: x_prime = F*x
    H:             measurement function: position = H*x
    '''
    R = 1000

    F = np.matrix([ [1., 0., 1., 0., 0., 0., 0., 0.], 
                    [0., 1., 0., 1., 0., 0., 0., 0.], 
                    [0., 0., 1., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 1., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 1., 0., 1., 0.], 
                    [0., 0., 0., 0., 0., 1., 0., 1.], 
                    [0., 0., 0., 0., 0., 0., 1., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 1.] ])
    
    H = np.matrix([ [1., 0., 0., 0., 0., 0., 0., 0.], 
                    [0., 1., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 1., 0., 0., 0.], 
                    [0., 0., 0., 0., 0., 1., 0., 0.] ])

    # prediction
    x = (F * x) 
    P = F * P * F.T
    
    # correct - measurement update
    measurement = measurement[..., np.newaxis]
    y = measurement - (H * x)
    S = H * P * H.T + R*np.eye(4)
    K = P * H.T * S.I
    x = x + (K * y)
    I = np.matrix(np.eye(F.shape[0]))
    P = (I - (K * H)) * P    

    return x, P