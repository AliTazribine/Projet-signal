# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:37:12 2021

@author: 190356
"""

import Utils
import audiofile
import numpy as np


speaker_man = Utils.get_random_speakers('bdl')
speaker_woman = Utils.get_random_speakers('slt')
speakers=speaker_man+speaker_woman
#on transforme les fichiers en signaux
for i in (speakers):
    info_signal=audiofile.read(i)
    signal=info_signal[0]
    fs=info_signal[1]
    normalized_signal=Utils.normalize(signal)
    print(normalized_signal)
    splitted_signal=Utils.split(normalized_signal, 50,50,fs)
    energies=[]
    for j in splitted_signal:
        energy=Utils.compute_energy(i)
        energies.append(energy)
    th=Utils.get_threshold(energies)
    voiced_frames=[]
    for j in range(len(energies)):
        if Utils.is_voiced(None, th,energies[i]):
            voiced_frames.append(splitted_signal[i])
    for j in voiced_frames:
        freq_resp=np.fft.fft(j)
        logfft=np.log10(freq_resp)
        cepstrum=np.fft.ifft(logfft)
    
    listf0=[]
    for j in splitted_signal:
        if j in voiced_frames:
            None
        else:
            listf0.append(0)
    
