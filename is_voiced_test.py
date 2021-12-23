# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:20:03 2021

@author: 190356
"""

import Utils

th=160
signal=[15,45,54,32,10]

test=Utils.is_voiced(signal, th)
if((15+45+54+32+10<160) == test):
    print("le calcul est bon")
