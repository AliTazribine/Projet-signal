# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:37:12 2021

@author: 190356
"""

import Utils
import audiofile
import numpy as np
#import matplotlib.pyplot as plt

#On compare a peu près les différentes valeurs obtenues entre les hommes et les femmes
def rule_based_system_observation():
    speakers_man = Utils.get_random_speakers('bdl',15)
    speakers_woman = Utils.get_random_speakers('slt',15)
    pitch_list=Utils.pitch_cepstrum(speakers_man,speakers_woman)
    c1=0
    c2=0
    for i in range(len(speakers_woman)):
       signal = audiofile.read(speakers_woman[i])
       formants=Utils.formants(signal[0],35,35,signal[1])
       formant=formants[0]
       pitch=pitch_list[i]
       print("women"+str(i+1))
       c1,c2=rules(formant,pitch,c1,c2,False)
       print("")
       #print('men'+str(i+1)+' : formant='+str(formant)+'  pitch='+str(pitch))
    for i in range(len(speakers_man)):
        signal = audiofile.read(speakers_man[i])
        formants = Utils.formants(signal[0], 35, 35, signal[1])
        formant = formants[0]
        pitch=pitch_list[len(speakers_man)+i]
        print("man"+str(i+1))
        c1,c2=rules(formant,pitch,c1,c2,True)
        print("")
        #print('women' + str(i+1) + ' : formant=' + str(formant)+'  pitch='+str(pitch))
    print("Résultat test formant en % :"+str(c1/(len(speakers_man)+len(speakers_woman))*100))
    print("Résultat test pitch en % :" + str(c2 / (len(speakers_man) + len(speakers_woman)) * 100))

#On va donc définir nos règles à partir du formant et du pitch :
def rules(formant,pitch,formantok,pitchok,man):

    if(formant<600):
        print("Following the formant, the speaker seems to be a women")
        if(not man):
            formantok+=1
    else :
        print("Following the formant, the speaker seems to be a man")
        if(man):
            formantok+=1


    if(pitch < 200):
        print("Following the pitch, the speaker seems to be a man")
        if (man):
            pitchok += 1
    else:
        print("Following the pitch, the speaker seems to be a women")
        if (not man):
            pitchok += 1
    return formantok,pitchok

def rule_based_system(formant, pitch):
    c1=0
    c2=0
    rules(formant,pitch,c1,c2)
rule_based_system_observation()