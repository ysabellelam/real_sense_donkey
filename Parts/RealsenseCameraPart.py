# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 22:41:53 2019
@author: Jordan, William, Ysabelle
"""

import cv2
import time
from pyrealsense2 import pipeline,colorizer,config,stream,format,hole_filling_filter,spatial_filter,temporal_filter,option
import numpy as np



class RealsenseCameraPart(object):

    def __init__(self, image_w=640, image_h=480, image_d=3,compress_depth=True):
        self.combined_array = None
        self.compress_depth = compress_depth
        self.running = True
        self.image_w = image_w
        self.image_h = image_h
        #self.depth, self.color = None, None

        #Set stream speed and resolution
        self.fps = 30
        #start post processing
        self.colorizer = colorizer()
        self.holefiller = hole_filling_filter(1)
        self.spatial = spatial_filter()
        self.temporal = temporal_filter()
        #start the Realsense pipeline
        self.pipe = pipeline()
        #load the configuration
        cfg = config()
        cfg.enable_stream(stream.color,stream_index=-1,width=848,height=480,framerate=30)
        cfg.enable_stream(stream.depth, stream_index=-1,width=848,height=480,framerate=30)
        #start the pipeline
        profile = self.pipe.start(cfg)
        #set units to 100um
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_sensor.set_option(option.depth_units,0.0001)

    def poll(self):
        frame_data = self.pipe.wait_for_frames()

        depth = frame_data.get_depth_frame()
        #post process depth frame
        depth = self.spatial.process(depth)
        depth = self.temporal.process(depth)
        depth = self.holefiller.process(depth)
        
        color = frame_data.get_color_frame()
        color_data = np.array(color.get_data())
        #run the below line if red and blue are flipped
#        color_data = cv2.cvtColor(color_data, cv2.COLOR_BGR2RGB)
        
        if self.compress_depth:
          depth_data = np.uint8(np.array(depth.get_data())//256)
          depth_data_compressed = np.dstack((depth_data[:160,:],depth_data[160:320,:],depth_data[320:480,:]))
          combined_raw = cv2.vconcat((color_data,depth_data_compressed))
        else:
          depth_data_c = colorizer.colorize(depth)
          combined_raw = cv2.vconcat((color_data,depth_data_c))
        
        self.combined_array = cv2.resize(combined_raw,(self.image_w,self.image_h),interpolation=cv2.INTER_NEAREST)
        
        
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
