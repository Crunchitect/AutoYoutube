from gtts import gTTS
from os import mkdir


get_script = "\"wow\"so hello\"but\"nevermind"

try:
    mkdir('resources')
except FileExistsError:
    pass

gtts_filter = str(get_script)
gtts_filter = gtts_filter.replace("\"", "♦")
gtts_speech = ''
remove_from_gtts = False
for i in gtts_filter:
    remove_from_gtts = not remove_from_gtts if i == "♦" else remove_from_gtts
    gtts_speech += i if not remove_from_gtts else ''
print(gtts_speech)
tts = gTTS(gtts_speech)
tts.save('resources/tts.mp3')
