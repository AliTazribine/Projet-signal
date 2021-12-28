# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:20:03 2021

@author: 190356
"""

import Utils

th=30
signal1=[1,2,3,4]
resp1=False
signal2=[23,34,43,23]
resp2=True

test1=Utils.is_voiced(signal1, th)
test2=Utils.is_voiced(signal2, th)

if(test1==resp1 and test2==resp2):
    print("Cette fonction détecte bien si un signal est voisé")

