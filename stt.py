# import user config
from config import LOG

# import pytorch
import torch
import torchaudio

# import speechbrain
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio, write_audio

# speechbrain stt libs
from speechbrain.pretrained import EncoderDecoderASR

# import tqdm
from tqdm import tqdm

# initialize the decoder
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-crdnn-rnnlm-librispeech", 
    savedir="pretrained_models/asr-crdnn-rnnlm-librispeech"
)

def save_waveform(path, waveform, rate=22050):

    # save
    write_audio(path, waveform, rate)

    # log
    if LOG:
        print(f'INFO: Waveform saved at {path}')


def run():
    
    # log
    if LOG:
        print('INFO: Starting')

    # init
    path = f"./waveforms/speechbrain_enchanced.wav"

    # run
    text = asr_model.transcribe_file(path)

    print(text)


# run
run()
