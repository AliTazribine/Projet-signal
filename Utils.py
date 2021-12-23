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

def get_random_speakers(gender,nbr=5):
    """
    Parameters
    ----------
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

def get_threshold(list_energies):
    """
    Parameters
    ----------
    list_energies : array_like
        contains the energy of each frame
    ----------
    """
    th=None
    i=1
    while(i<len(list_energies)-1):
        if(list_energies[i]>list_energies[i-1] and list_energies[i]> list_energies[i+1]):
            if(th != None):
               if (list_energies[i]>th):
                   th=list_energies[i]
            else:
                th=list_energies[i]
        i+=1
    return th

def formants(signal,width,slidingstep,fs):
    frames=split(signal, width, slidingstep, fs)
    b,a=[1,0.67],[1,0]
    #filtered_frames=[]
    roots=[]
    for frame in frames :
        filtered_frame=sp.lfilter(b,a,frame)
        win=np.hamming(len(filtered_frame))
        filtered_frame=filtered_frame*win
        #filtered_frames.append(filtered_frame)
        lpc_coeff=lpc.lpc_ref(filtered_frame, 12)
        root=np.roots(lpc_coeff)
        for i in range(len(root)):
            im=np.imag(root[i])
            if(im>0):
                roots.append(root[i])
    angles=np.arctan2(np.imag[roots], np.real(roots))
    frequencies=sorted(angles*fs/2*np.pi)
    return frequencies

def rule_based_system():
    speaker_man = get_random_speakers('bdl',15)
    speaker_woman = get_random_speakers('slt',15)
    for i in speaker_man :
        info_signal=audiofile.read(i)
        signal=info_signal[0]
        fs=info_signal[1]
        print("man formants : "+str(formants(signal,35,35,fs)))
    for i in speaker_woman:
        info_signal=audiofile.read(i)
        signal=info_signal[0]
        fs=info_signal[1]
        print("woman formants:"+str(formants(signal,35,35,fs)))
    
        
        
    