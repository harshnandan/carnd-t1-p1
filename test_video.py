# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML
from line_marker import *
import os

class image_processor_class():
    def __init__(self, clip, outputFile):
        videoClip = clip
        
        self.line_state = np.zeros((8, 1))
        self.line_uncertanity = np.zeros((8,8))
        self.line_uncertanity[0, 0] = 1
        self.line_uncertanity[1, 1] = 1
        self.line_uncertanity[2, 2] = 1000
        self.line_uncertanity[3, 3] = 1000
        self.line_uncertanity[4, 4] = 1
        self.line_uncertanity[5, 5] = 1
        self.line_uncertanity[6, 6] = 1000
        self.line_uncertanity[7, 7] = 1000
        
        white_clip = videoClip.fl_image(self.process_image) 
        white_clip.write_videofile(outputFile, audio=False)        
    
    def process_image(self, image):
        result = lineMarkerFnc(image, self.line_state, self.line_uncertanity)
        self.line_state, self.line_uncertanity = result['lines']
        return result['img']

# fileName = 'solidWhiteRight.mp4'
# fileName = 'solidYellowLeft.mp4'
fileName = 'challenge.mp4'

# fileList = os.listdir("test_videos/")
# for figIdx, fileName in enumerate(fileList):

inputFile = 'test_videos/' + fileName
outputFile = 'test_videos_output/' + fileName

# clip1 = VideoFileClip(inputFile).subclip(0, 5)
clip1 = VideoFileClip(inputFile)

oImageProc = image_processor_class(clip1, outputFile)
# white_clip = clip1.fl_image(oImageProc.process_image) 
# white_clip.write_videofile(outputFile, audio=False)

