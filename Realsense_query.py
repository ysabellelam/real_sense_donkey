# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:32:47 2019

@author: Jordan
"""
from pyrealsense2 import context
ctx = context()

print(ctx.query_devices())
for dev in ctx.query_devices():
  print(dev.get_info)
  print(dev.query_sensors)
  for dev2 in dev.query_sensors():
    print(dev.get_info)