# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML
from line_marker import *
import os

def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    result = lineMarkerFnc(image)
    return result

fileName = 'solidWhiteRight.mp4'
fileName = 'solidYellowLeft.mp4'
# fileName = 'challenge.mp4'

# fileList = os.listdir("test_videos/")
# for figIdx, fileName in enumerate(fileList):

inputFile = 'test_videos/' + fileName
outputFile = 'test_videos_output/' + fileName

# clip1 = VideoFileClip(inputFile).subclip(0, 6)
clip1 = VideoFileClip(inputFile)

white_clip = clip1.fl_image(process_image) 
white_clip.write_videofile(outputFile, audio=False)

