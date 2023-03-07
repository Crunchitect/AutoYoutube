from pyChatGPT import ChatGPT
from creds import session_token
from random import randint
from gtts import gTTS

api = ChatGPT(session_token)

resp = api.send_message(f'Can you give me a YouTube video script for a 1'
                        f'-minute coding video with code snippets included?')
get_script = resp['message']
print(resp['message'])

gtts_filter = str(get_script)
gtts_filter.replace("```", "♦")
gtts_speech = ''
remove_from_gtts = False
for i in gtts_filter:
    remove_from_gtts = not remove_from_gtts if i == "♦" else remove_from_gtts
    gtts_speech += i if not remove_from_gtts else ''
print(gtts_speech)
tts = gTTS(gtts_speech)
tts.save('resources/tts.mp3')
