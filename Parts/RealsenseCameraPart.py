# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 22:41:53 2019

@author: Jordan
"""

import cv2
import time
from pyrealsense2 import pipeline,config,stream
import numpy as np



class RealsenseCameraPart(object):

    def __init__(self, image_w=640, image_h=480, image_d=4):
        self.combined_array = None
        self.running = True
        self.image_w = image_w
        self.image_h = image_h
        self.depth, self.color = None, None

        # Set stream speed and resolution
        self.fps = 30
        
        #start the Realsense pipeline
        self.pipe = pipeline()
        #load the configuration
        cfg = config()
        cfg.enable_stream(stream.color,stream_index=-1,width=640,height=480,framerate=30)
        cfg.enable_stream(stream.depth, stream_index=-1,width=640,height=480,framerate=30)
        self.pipe.start(cfg)

    def poll(self):
        frame_data = self.pipe.wait_for_frames()

        depth = frame_data.get_depth_frame()
        color = frame_data.get_color_frame()
        color_data = np.array(color.get_data())
#run the below line if red and blue are flipped
#        color_data = cv2.cvtColor(color_data, cv2.COLOR_BGR2RGB)
        depth_data = np.uint8(np.array(depth.get_data())//256)
        self.depth = cv2.resize(depth_data,(self.image_w,self.image_h))
        self.color = cv2.resize(color_data,(self.image_w,self.image_h))
        #3d image
		self.combined_array = np.dstack((self.color[:,:,0], self.color[:,:,2], self.depth))
		#4d image
		#self.combined_array = np.dstack((self.color, self.depth))
        
    def update(self):
        while self.running:
            self.poll()

    def run_threaded(self):
        return self.combined_array

    def run(self):
        self.poll()
        return self.combined_array

    def shutdown(self):
        self.running = False
        time.sleep(0.2)
        self.pipe.stop()


class CvImageDisplay(object):
    def run(self, image):
        cv2.imshow('frame', image)
        cv2.waitKey(1)

    def shutdown(self):
        cv2.destroyAllWindows()