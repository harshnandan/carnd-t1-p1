import os
from line_marker import *
import matplotlib.image as mpimg

fileList = os.listdir("test_images/")
print(fileList)
numFig = len(fileList)
for figIdx, fileName in enumerate(fileList):
    # read image
    image = mpimg.imread('./test_images/' + fileName)
    lineMarkerFnc(image, figIdx, numFig, (20, 8))