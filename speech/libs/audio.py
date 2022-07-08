"""
    Helpful functions to soften voice audio tracks
"""

# import libs
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
import torch
import torchaudio
import torchaudio.transforms as T

# config
SAMPLING_RATE = 16000


def resample(waveform, src_sampling=22050, dest_sampling=16000):
    resampler = T.Resample(src_sampling, dest_sampling, dtype=waveform.dtype)
    resampled_waveform = resampler(waveform)
    return resampled_waveform


def concatenate_waveforms(wav_1, wav_2):
    if wav_1 is None:
        wav_1 = torch.empty((0))
    if wav_2 is None:
        wav_2 = torch.empty((0))
    return torch.cat((wav_1, wav_2), 0)


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
