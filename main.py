# from gtts import gTTS
from transformers import pipeline, set_seed
from os import mkdir
import torchaudio
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN

# Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")

generator = pipeline('text-generation', model='gpt2-large')
set_seed(42)
get_script = generator('Hello Everyone, And welcome to another coding tutorial! Today we will talk about',
                       max_length=150)

get_script = get_script[0]["generated_text"]

try:
    mkdir('resources')
except FileExistsError:
    pass

# gtts_filter = str(get_script)
# gtts_filter = gtts_filter.replace("\"", "♦")
# gtts_speech = ''
# remove_from_gtts = False
# for i in gtts_filter:
#     remove_from_gtts = not remove_from_gtts if i == "♦" else remove_from_gtts
#     gtts_speech += i if not remove_from_gtts else ''
print(get_script)

# Running the TTS
mel_output, mel_length, alignment = tacotron2.encode_text(get_script)

# Running Vocoder (spectrogram-to-waveform)
waveforms = hifi_gan.decode_batch(mel_output)

# Save the waverform
torchaudio.save('resources/tts.wav',waveforms.squeeze(1), 22050)

# tts = gTTS(get_script)
# tts.save('resources/tts.mp3')
