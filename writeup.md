# **Finding Lane Lines on the Road** 

## Writeup

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. The pipeline is shown below with output for each step:
<img src="./pipeline_steps/step_0_original.png" width="480" alt="Combined Image"/>

* First, I converted the images to grayscale, 
<img src="./pipeline_steps/step_1_grayScale.png.png" width="480" alt="Combined Image"/>

* then I applied Gaussian Blur to reduce noise in the image so that Canny edge detection can pick up actual edges
<img src="./pipeline_steps/step_2_blur.png" width="480" alt="Combined Image"/>

* This was followed by Canny edge detection which detects the edges in the scene
<img src="./pipeline_steps/step_3_CannyEdge.png" width="480" alt="Combined Image"/>

* A mask was designed keeping in mind the perspective view of the lane, this helps to focus on region of interest when perform line detection using Hough transform.
<img src="./pipeline_steps/step_4_RegionInterest.png" width="480" alt="Combined Image"/>
<img src="./pipeline_steps/step_5_Lines.png" width="480" alt="Combined Image"/>

* A bitwise 'and' operation was  
<img src="./pipeline_steps/step_6_Superimposed.png" width="480" alt="Combined Image"/>

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
