from pyChatGPT import ChatGPT
from creds import session_token
from random import randint

api = ChatGPT(session_token)

resp = api.send_message(f'Can you give me 10 ideas for a {randint(1, 3)}-minute coding video?')
get_ideas = resp['message']
print(resp['message'])

resp = api.send_message(f'Can I see a script of #{randint(1, 10)}; Code snippets included, please.')
get_script = resp['message']
print(resp['message'])
