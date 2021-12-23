# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:04:03 2021

@author: 190356
"""

import Utils

speaker_woman1=Utils.get_random_speakers('slt',2)
speaker_woman2=Utils.get_random_speakers('slt',2)
print(speaker_woman1)
print(speaker_woman2)
if('slt' in speaker_woman1[0] and 'slt' in speaker_woman2[0]):
    print("les speakers sont bien des femmes")
    
if(speaker_woman1 != speaker_woman2):
    print("les speakers ont bien été choisi aléatoirement")