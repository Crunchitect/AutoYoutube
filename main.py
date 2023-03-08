from gtts import gTTS
from transformers import pipeline
from os import mkdir

generator = pipeline('text-generation', model='gpt2-large')
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

tts = gTTS(get_script)
tts.save('resources/tts.mp3')

print(get_script)
