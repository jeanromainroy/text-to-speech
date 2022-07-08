"""
    Helpful functions to soften voice audio tracks
"""

# import libs
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
import torch

# config
SAMPLING_RATE = 16000


def low_pass(xn, cutoff_freq=4000, order=3):

    # init order 3 lowpass butterworth filter
    b, a = signal.butter(order, cutoff_freq, btype='lowpass', fs=SAMPLING_RATE)

    # apply using filtfilt
    yn = signal.filtfilt(b, a, xn)

    return yn
    

def high_pass(xn, cutoff_freq=96, order=3):

    # init order 3 lowpass butterworth filter
    b, a = signal.butter(order, cutoff_freq, btype='highpass', fs=SAMPLING_RATE)

    # apply using filtfilt
    yn = signal.filtfilt(b, a, xn)

    return yn


def bandstop(xn, cutoff_freq=[1000, 1400], order=3):

    # init order 3 lowpass butterworth filter
    b, a = signal.butter(order, cutoff_freq, btype='bandstop', fs=SAMPLING_RATE)

    # apply using filtfilt
    yn = signal.filtfilt(b, a, xn)

    return yn


def volume(xn, factor=2):
    return xn * factor


def equalize(waveform):

    # convert 1D tensor to numpy array
    xn = waveform.numpy()

    # apply high pass
    xn = high_pass(xn)

    # apply bandstop
    xn = bandstop(xn)

    # increase volume
    xn = volume(xn)
    
    # convert numpy array to 1D tensor
    waveform_eq = torch.from_numpy(xn.copy())

    # set type
    waveform_eq = waveform_eq.type(torch.float32)

    return waveform_eq
