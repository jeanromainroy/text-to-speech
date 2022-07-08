"""
    Text-to-Speech module

    info: tts does ~4 syllables / second
"""

# import user config
from config import LOG, MAX_NBR_OF_CHARS_PER_WAVEFORM

# import speechbrain
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio, write_audio

# speechbrain enhancement libs
from speechbrain.pretrained import SpectralMaskEnhancement
from speechbrain.pretrained import WaveformEnhancement

# speechbrain tts libs
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN

# import tqdm
from tqdm import tqdm

# import multi-thread
import threading

# import libs
from libs.chunker import chunk_text
from libs.audio import equalize, resample
from libs.strings import generate_uuid
from libs.player import Player


# intialize TTS (tacotron2) and Vocoder (HiFIGAN)
tacotron2 = Tacotron2.from_hparams(
    source="speechbrain/tts-tacotron2-ljspeech", 
    savedir="tmp/tts"
)

hifi_gan = HIFIGAN.from_hparams(
    source="speechbrain/tts-hifigan-ljspeech", 
    savedir="tmp/vocoder"
)

# initialize the enhancers
enhance_model = WaveformEnhancement.from_hparams(
    source="speechbrain/mtl-mimic-voicebank",
    savedir="tmp/pretrained_models/mtl-mimic-voicebank",
)


def text_to_waveform(text):

    # Running the TTS
    mel_output, mel_length, alignment = tacotron2.encode_text(text)

    # Running Vocoder (spectrogram-to-waveform)
    waveforms = hifi_gan.decode_batch(mel_output)

    # Flatten
    waveform = waveforms.detach().cpu().squeeze()
    
    return waveform


def enhance_waveform(waveform):

    # enhance
    waveform_enhanced = enhance_model.enhance_batch(waveform.unsqueeze(0)).detach().cpu().squeeze()

    # traditionnal audio processing to soften the track
    waveform_enhanced = equalize(waveform_enhanced)

    return waveform_enhanced


def save_waveform(path, waveform, rate=22050):

    # save
    write_audio(path, waveform, rate)

    # log
    if LOG: print(f'INFO: Waveform saved at {path}')


def run(text):
    
    # log
    if LOG: print('INFO: Starting')

    # init
    waveform_files = []

    # chunk text
    chunks = chunk_text(text, MAX_NBR_OF_CHARS_PER_WAVEFORM, LOG=LOG)

    # create uid for each chunk
    chunks_uid = [generate_uuid() for chunk in chunks]

    # init player
    player = Player(chunks_uid)

    # Create a Thread with a function without any arguments
    th = threading.Thread(target=player.start)

    # Start the thread
    th.start()
    
    # convert text to waveform
    for i, text in enumerate(chunks):

        # create file path
        path = f"./tmp/{chunks_uid[i]}.wav"

        # convert chunk to waveform
        waveform = text_to_waveform(text)

        # resample
        waveform_resampled = resample(waveform, 22050, 16000)

        # enhance
        waveform_enhanced = enhance_waveform(waveform_resampled)

        # save
        save_waveform(path, waveform_enhanced, rate=16000)

        # append
        waveform_files.append(path)

        # log
        if LOG: print(f'INFO: File saved at {path}')

    # Wait for thread to finish
    th.join()
