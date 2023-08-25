import os
import json
from oaisdk import OaiSDK

import logging
OaiSDK.setLogLevel(logging.DEBUG)

OaiSDK.auth(open(f"._osecret", "r").readlines()[0].strip())

model_id = "gpt-3.5-turbo"

chat = OaiSDK.resource('chat')
response = chat.completions({
        "model": model_id,
        "messages": [{"role": "user", "content": "What is ChatGPT?"}],
        "temperature": 0.7
   })
print(json.dumps(response, indent=4))
