import os
from line_marker import *
import matplotlib.image as mpimg

fileList = os.listdir("test_images/")
numFig = len(fileList)
for figIdx, fileName in enumerate(fileList):
    # read image
    image = mpimg.imread('./test_images/' + fileName)
    out_image = lineMarkerFnc(image, figIdx, numFig, (20, 8))
    cv2.imwrite('./test_images_output/' + fileName, cv2.cvtColor(out_image,cv2.COLOR_RGB2BGR))