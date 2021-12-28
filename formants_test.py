# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:42:38 2021

@author: 190356
"""

import Utils
import audiofile

speaker=Utils.get_random_speakers('slt',1)
sig,fs=audiofile.read(speaker[0])

formant_list=Utils.formants(sig, 30, 30, fs)
sort=True

for i in range(len(formant_list)-1):
    if(i==0):
        if(formant_list[i]>formant_list[i+1]):
            sort=False
    else:
        if(formant_list[i]<formant_list[i-1] or formant_list[i]>formant_list[i+1]):
            sort=False
if(sort):
    print("La liste de formants est bien triée")