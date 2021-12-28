# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 15:33:03 2021

@author: 190356
"""

import Utils
import numpy as np

signal=[1,2,3,4,5,6]
liste1=np.array([[1,2],[3,4],[5,6]])
width=2
sstep=2
fs=1000
liste2=Utils.split(signal,width,sstep,fs)
ok=True

for i in range(len(liste1)) :
    for j in range(len(liste1[i])):
        if(liste1[i][j]!=liste2[i][j]):
            ok=False
if ok:
    print("La fonction divise bien la liste"+str(signal))
else :
    print("Il y'a une erreur dans la division")