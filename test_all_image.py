import os
from line_marker import *
import matplotlib.image as mpimg

fileList = os.listdir("test_images/")
numFig = len(fileList)

line_state = np.array([0, 0, 0, 0])
line_uncertanity = np.zeros((8,8))
line_uncertanity[0] = 1
line_uncertanity[1] = 1
line_uncertanity[2] = 1000
line_uncertanity[3] = 1000
line_uncertanity[4] = 1
line_uncertanity[5] = 1
line_uncertanity[6] = 1000
line_uncertanity[7] = 1000

for figIdx, fileName in enumerate(fileList):
    # read image
    image = mpimg.imread('./test_images/' + fileName)
    out_image = lineMarkerFnc(image, line_state, line_uncertanity)
    cv2.imwrite('./test_images_output/' + fileName, cv2.cvtColor(out_image['img'],cv2.COLOR_RGB2BGR))