# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 22:47:57 2019

@author: Jordan
"""

from pyrealsense2 import pipeline,colorizer
import cv2
import numpy as np

#initialize the pipeline
RSpipeline = pipeline()
RScolorizer = colorizer()
#start the pipeline, might need to load a configuration file
RSpipeline.start()

frame_data = RSpipeline.wait_for_frames()
depth = frame_data.get_depth_frame()
color = frame_data.get_color_frame()

print('depth width',depth.get_width())
print('depth height',depth.get_height())
print('color width',color.get_width())
print('color height',color.get_height())

depth_c = RScolorizer.colorize(depth)
depth_data = np.array(depth_c.get_data())

frame_index = 1
save_image = False


#loop 1000 times to get several images and make the appearance of a video
for i in range(1000):
  #Wait for the next frame
  frame_data = RSpipeline.wait_for_frames()
  #get depth and color frames from the stream frame
  depth = frame_data.get_depth_frame()
  color = frame_data.get_color_frame()
  depth_c = RScolorizer.colorize(depth)
  color_data = np.array(color.get_data())
  depth_data = np.array(depth_c.get_data())
  #use this for showing the color image
  #cv2.imshow('color',cv2.cvtColor(data, cv2.COLOR_BGR2RGB))
  #use this to display the depth image
  cv2.imshow('depth',depth_data)
  key = cv2.waitKey(1) & 255
  
  if chr(key) == 's':
    print("\t s key detected. Saving image.")
    save_image = True
    cv2.imwrite('colorized_depth_'+ str(frame_index) + ".PNG",depth_data)

  save_image = False
  frame_index += 1
    

RSpipeline.stop()