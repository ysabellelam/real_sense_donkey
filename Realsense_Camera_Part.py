# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 22:41:53 2019

@author: Jordan
"""

import cv2
import time
from pyrealsense2 import pipeline
import numpy as np



class RealsenseCameraPart(object):

    def __init__(self, image_w=1280, image_h=720, image_d=4,framerate=30):
        self.combined_array = None
        self.running = True
        self.image_w = image_w
        self.image_h = image_h
        self.framerate = framerate
        self.depth, self.color = None, None

        # Set stream speed and resolution
        self.fps = 30
        
        #start the Realsense pipeline
        self.pipe = pipeline()
        #load the configuration
        cfg = config()
        cfg.enable_stream(stream.color,stream_index=-1,width=image_w,height=image_h,framerate=framerate)
        cfg.enable_stream(stream.depth, stream_index=-1,width=image_w,height=image_h,framerate=framerate)
        self.pipe.start(cfg)
        
#    def get_depth(self):
#        """
#        Returns numpy ndarrays representing the raw and ranged depth images.
#        Outputs:
#            dmap: distance map in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
#            d4d:  depth for display, 3L ndarray, dtype=uint8, min=0, max=255
#        """
#        dmap = np.frombuffer(self.depth_stream.read_frame().get_buffer_as_uint16(), dtype=np.uint16).reshape(self.image_h, self.image_w)
#        d4d = np.uint8(dmap.astype(float) * 255 / 2 ** 12 - 1)
#        d4d = cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
#        # d4d = np.dstack((d4d, d4d, d4d))
#
#        return dmap, d4d

#    def get_color(self):
#        """
#        Returns numpy ndarrays representing raw and ranged infra-red(IR) images.
#        outputs:
#            ir  : raw IR, 1L ndarrya, dtype=uint16, min=0, max=2**12-1
#            ir4d: IR for display, 3L ndarray, dtype=uint8, min=0, max=255
#        """
#        ir_frame = self.ir_stream.read_frame()
#        ir_frame_data = self.ir_stream.read_frame().get_buffer_as_uint16()
#        ir4d = np.ndarray((ir_frame.height, ir_frame.width), dtype=np.uint16, buffer=ir_frame_data).astype(np.float32)
#        ir4d = np.uint8((ir4d / ir4d.max()) * 255)
#        ir4d = cv2.cvtColor(ir4d, cv2.COLOR_GRAY2RGB)
#        return ir_frame, ir4d

    def poll(self):
        frame_data = self.pipe.wait_for_frames()

        depth = frame_data.get_depth_frame()
        color = frame_data.get_color_frame()
        color_data = np.array(color.get_data())
#run the below line if red and blue are flipped
#        color_data = cv2.cvtColor(color_data, cv2.COLOR_BGR2RGB)
        depth_data = np.array(depth.get_data())
        self.depth = cv2.resize(depth_data,(self.image_w,self.image_h))
        self.color = cv2.resize(color_data,(self.image_w,self.image_h))
        self.combined_array = np.dstack((self.color, self.depth))
        
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