# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 13:42:55 2021

@author: Ali Tazribine
"""
import math

import numpy as np
import random as rnd
import scipy as sp
import glob
import audiofile
import scikit_talkbox_lpc as lpc

"""The signal’s sample values are scaled between a
certain range (in this case, we’ll scale it between -1 and 1)"""
def normalize(signal):
    """
    Parameters
    ----------
    signal: array_like
       the input signal
    ----------
    """
    return signal/np.max(np.abs(signal))
    
"""The speech segment is split in (non-)overlapping frames. In-
deed, in order to obtain values that represents signals as precisely as
possible, we need to extract features from slices (referred to as frames )
of the signal"""
def split(signal,width,slidingstep,fs):
    """
    Parameters
    ----------
    signal : array_like
        the input signal
    width: int
        the width of the window [ms]
    slidingstep : int
        the sliding step of the window [ms]
    fs: float
        the sampling frequency
    ----------
    """
    output=[]
    nsliding = int(slidingstep/1000*fs)
    n=int(np.size(signal)/nsliding)
    nwidth= int(width/1000*fs)
    for i in range(n):
        if((i*nsliding)+nwidth > np.size(signal)):
            frame=signal[i*nsliding:(i*nsliding)+nwidth-(((i*nsliding)+nwidth)-np.size(signal))]
            output.append(frame)
        else:
            frame=signal[i*nsliding:(i*nsliding)+nwidth]
            output.append(frame)
    output=np.array(output)
    return output

"""The energy of a signal is computed"""
def compute_energy(signal):
    """
    Parameters
    ----------
    signal : array_like
        the input signal
    ----------
    """
    sum=0
    i=0
    while(i<len(signal)):
        x=(abs(signal[i])**2)
        sum+=x
        i+=1
    return sum

"""This function return a list of paths of random speakers"""
def get_random_speakers(gender,nbr=5):
    """
    Parameters
    ----------
    gender : String
        the gender of the speaker
    nbr : int
        numbers of files to choose
    ----------
    """
    path=glob.glob('cmu_us_'+gender+'_arctic/wav/*.wav')
    list_path=rnd.sample(range(len(path)-1),nbr) #on choisit 5 fichier parmis ceux dans path
    speakers=[]
    for i in list_path:
        speakers.append(path[i])
    return speakers

"""This function return True if the signal is voiced"""
def is_voiced(signal,th,energy=None):
    """
    Parameters
    ----------
    signal : array_like
        the input signal
    th : float
        the threshold
    energy : float
        the energy of the signal
    ----------
    """
    if (energy==None):
        energy=compute_energy(signal)
    return energy>th


"""Compute the pitch of the signals of the speakers"""
def pitch_cepstrum(speakers) :
    """
    Parameters :
        speakers : list
            contient les audios pour lesquels il faut calculer le pitch
    """
    maxf0speaker=[]
    #on transforme les fichiers en signaux
    for i in (speakers):
        info_signal=audiofile.read(i)
        signal=info_signal[0]
        fs=info_signal[1]
        #On normalise le signal
        normalized_signal=normalize(signal)
        #plt.plot(normalized_signal)
        #On le divise
        splitted_signal=split(normalized_signal, 50,50,fs)
        energies=[]
        #On crée une liste avec l'énergie de toutes les frames
        for j in splitted_signal:
            energy=compute_energy(j)
            energies.append(energy)
        #On choisi un seuil(graphiquement)
        th=15
        voiced_frames=[]
        #On crée une liste avec les indices des "voiced_frames"
        for j in range(len(energies)):
            if is_voiced(None, th,energies[j]):
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
        k=0
        for j in range(len(splitted_signal)):
            if j in voiced_frames:
                max_cep=max(cepstrum_list[k])
                k+=1
                angle=(np.arctan2(np.imag(max_cep), np.real(max_cep)))
                freq=angle*fs/2*np.pi
                if(freq<50):
                    listf0.append(50)
                else:
                    listf0.append(freq)
            else:
                listf0.append(0)
        #print(listf0)
        maxf0speaker.append(max(listf0))
    return maxf0speaker

"""Compute the formants of a signal"""
def formants(signal,width,slidingstep,fs):
    """
    Parameters :
        signal : array_like
            the signal
        width: int
            the width of the window [ms] for the splitting
        slidingstep : int
            the sliding step of the window [ms] for the splitting
        fs: float
            the sampling frequency for the splitting
    """
    frames=split(signal, width, slidingstep, fs)
    b,a=[1,0.67],[1,0]
    #filtered_frames=[]
    roots=[]
    for frame in frames :
        filtered_frame=sp.signal.lfilter(b,a,frame)
        win=np.hamming(len(filtered_frame))
        filtered_frame=filtered_frame*win
        #filtered_frames.append(filtered_frame)
        lpc_coeff=lpc.lpc_ref(filtered_frame, 12)
        root=np.roots(lpc_coeff)
        for i in range(len(root)):
            im=np.imag(root[i])
            if(im>0):
                roots.append(root[i])
    angles=np.arctan2(np.imag(roots), np.real(roots))
    frequencies=sorted(angles*fs/2*np.pi)
    return frequencies
    
        
        
    