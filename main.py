from pyChatGPT import ChatGPT
from creds import session_token

api = ChatGPT(session_token)

resp = api.send_message('Hello, world!')
print(resp['message'])
api.clear_conversations()
