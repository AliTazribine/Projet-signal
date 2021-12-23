# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 15:33:03 2021

@author: 190356
"""

import Utils
import numpy as np

signal=[1,2,3,4,5,6]
liste=np.array([[1,2],[3,4],[5,6]])
width=2
sstep=2
fs=1000
print(Utils.split(signal,width,sstep,fs)==liste)