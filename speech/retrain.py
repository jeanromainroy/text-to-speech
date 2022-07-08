# import pytorch
import torch
import torchaudio

# import speechbrain
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio, write_audio
from speechbrain.dataio.dataset import DynamicItemDataset

# speechbrain stt libs
from speechbrain.pretrained import EncoderDecoderASR

# import tqdm
from tqdm import tqdm

# import class
from libs.EncDecFineTune import EncDecFineTune

# import parse data
# from parse_data import parse_to_json

# initialize the decoder
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-crdnn-rnnlm-librispeech", 
    savedir="tmp/pretrained_models/asr-crdnn-rnnlm-librispeech"
)

# path to LibriSpeech
path_librispeech = './tmp/LibriSpeech/dev-clean-2'

# parse 
# parse_to_json(path_librispeech)

# initialize the dataset
dataset = DynamicItemDataset.from_json("data.json")

# we limit the dataset to 100 utterances to keep the trainin short in this Colab example
dataset = dataset.filtered_sorted(sort_key="length", select_n=1)

# add read audio pipeline
dataset.add_dynamic_item(sb.dataio.dataio.read_audio, takes="file_path", provides="signal")

# define text pipeline
@sb.utils.data_pipeline.takes("words")
@sb.utils.data_pipeline.provides("words", "tokens_list", "tokens_bos", "tokens_eos", "tokens")
def text_pipeline(words):
      yield words
      tokens_list = asr_model.tokenizer.encode_as_ids(words)
      yield tokens_list
      tokens_bos = torch.LongTensor([asr_model.hparams.bos_index] + (tokens_list))
      yield tokens_bos
      tokens_eos = torch.LongTensor(tokens_list + [asr_model.hparams.eos_index]) # we use same eos and bos indexes as in pretrained model
      yield tokens_eos
      tokens = torch.LongTensor(tokens_list)
      yield tokens

# add text pipeline
dataset.add_dynamic_item(text_pipeline)

# set return keys
dataset.set_output_keys(["id", "signal", "words", "tokens_list", "tokens_bos", "tokens_eos", "tokens"])

# hyperparams
modules = {
    "enc": asr_model.mods.encoder.model, 
    "emb": asr_model.hparams.emb,
    "dec": asr_model.hparams.dec,
    "compute_features": asr_model.mods.encoder.compute_features, # we use the same features 
    "normalize": asr_model.mods.encoder.normalize,
    "seq_lin": asr_model.hparams.seq_lin,
}

hparams = {
    "seq_cost": lambda x, y, z: sb.nnet.losses.nll_loss(x, y, z, label_smoothing = 0.1),
    "log_softmax": sb.nnet.activations.Softmax(apply_log=True)
}

# init class
brain = EncDecFineTune(modules, hparams=hparams, opt_class=lambda x: torch.optim.SGD(x, 1e-5))
brain.tokenizer = asr_model.tokenizer

# train
brain.fit(range(2), train_set=dataset, train_loader_kwargs={"batch_size": 8, "drop_last":True, "shuffle": False})

# save
brain.evaluate(dataset)
