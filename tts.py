# import user config
from config import text as user_provided_text, LOG, MAX_NBR_OF_CHARS_PER_WAVEFORM

# import pytorch
import torch
import torchaudio

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

# import libs
from libs.chunker import chunk_text
from libs.audio import equalize
from libs.strings import generate_uuid


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


def enhance_waveform(path):

    # enhance
    waveform_enhanced = enhance_model.enhance_file(path).detach().cpu().squeeze()

    # traditionnal audio processing to soften the track
    waveform_enhanced = equalize(waveform_enhanced)

    return waveform_enhanced


def concatenate_waveforms(wav_1, wav_2):
    return torch.cat((wav_1, wav_2), 0)


def save_waveform(path, waveform, rate=22050):

    # save
    write_audio(path, waveform, rate)

    # log
    if LOG:
        print(f'INFO: Waveform saved at {path}')


def run(text):
    
    # log
    if LOG:
        print('INFO: Starting')

    # init
    waveform = torch.empty((0))

    # chunk text
    chunks = chunk_text(text, MAX_NBR_OF_CHARS_PER_WAVEFORM, LOG=LOG)

    # convert text to waveform
    for text in tqdm(chunks, disable=(not LOG)):

        # convert chunk to waveform
        waveform_chunk = text_to_waveform(text)

        # concatenate
        waveform = concatenate_waveforms(waveform, waveform_chunk)

    # save
    path = f"./tmp/{generate_uuid()}.wav"
    save_waveform(path, waveform, rate=22050)

    # enhance
    waveform_enhanced = enhance_waveform(path)

    # save
    path = f"./tmp/{generate_uuid()}.wav"
    save_waveform(path, waveform_enhanced, rate=16000)

    # log
    if LOG:
        print(f'File saved at {path}')


# run
run(user_provided_text)