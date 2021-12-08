import Utils as utils

"""The cepstrum-based algorithm to estimate the pitch"""
def cbp_estimation(signal,fs,slidingstep):
    """
    Parameters
    ----------
    signal : array_like
        the input signal
    fs: float
        the sampling frequency
    th: float
        the treshold determinated graphically (need to include the computation 
        in the code (not a real parameter of the function))
    ----------
    """
    norm=utils.normalize(signal)
    split_signal=utils.split(norm,50,slidingstep,fs)
    list_energy=[]
    for i in split_signal:
        list_energy.append(utils.compute_energy(i))
    th=utils.get_threshold(split_signal, list_energy)
    voiced_frames=[] #index of all voiced frames
    for frame in split_signal :
        energy=utils.compute_energy(frame)
        if(utils.is_voiced(frame,th,energy)):
            voiced_frames.append(frame)
        
    cepstrum_list=[] #the cepstrum of each voiced frame
    i=0