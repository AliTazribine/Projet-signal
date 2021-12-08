# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 13:42:55 2021

@author: Ali Tazribine
"""
import numpy as np
import random as rnd
import glob

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
    i=0
    while(i<n):
        if((i*nsliding)+nwidth > np.size(signal)):
            frame=signal[i*nsliding:(i*nsliding)+nwidth-(((i*nsliding)+nwidth)-np.size(signal))]
            output.append(frame)
        else:
            frame=signal[i*nsliding:(i*nsliding)+nwidth]
            output.append(frame)
        i+=1
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
        x=(np.abs(signal[i])**2)
        sum+=x
        i+=1
    return sum

def get_random_speaker(nbr=5):
    """
    Parameters
    ----------
    nbr : int
        numbers of files to choose
    ----------
    """
    path=glob.glob('./wav/*.wav')
    list_path=rnd.sample(range(len(path)-1,nbr)) #on choisit 5 fichier parmis ceux dans path
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
