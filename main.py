# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:37:12 2021

@author: 190356
"""

import Utils
import audiofile
import numpy as np
import matplotlib.pyplot as plt

speaker_man = Utils.get_random_speakers('bdl')
speaker_woman = Utils.get_random_speakers('slt')
speakers=speaker_man+speaker_woman
#on transforme les fichiers en signaux
for i in (speakers):
    info_signal=audiofile.read(i)
    signal=info_signal[0]
    fs=info_signal[1]
    #On normalise le signal
    normalized_signal=Utils.normalize(signal)
    plt.plot(normalized_signal)
    #On le divise
    splitted_signal=Utils.split(normalized_signal, 50,50,fs)
    energies=[]
    #On crée une liste avec l'énergie de toutes les frames
    for j in splitted_signal:
        energy=Utils.compute_energy(j)
        energies.append(energy)
    #On calcule un seuil
    th=Utils.get_threshold(energies)
    voiced_frames=[]
    #On crée une liste avec les indices des "voiced_frames"
    for j in range(len(energies)):
        if Utils.is_voiced(None, th,energies[j]):
            voiced_frames.append(j)
    #On calcule le cepstrum des voiced frames
    cepstrum_list=[]
    for j in voiced_frames:
        freq_resp=np.fft.fft(splitted_signal[j])
        logfft=np.log10(freq_resp)
        cepstrum=np.fft.ifft(logfft)
        cepstrum_list.append(cepstrum)
    #On calcule les f0
    listf0=[]
    for j in splitted_signal:
        if j in voiced_frames:
            None
        else:
            listf0.append(0)
