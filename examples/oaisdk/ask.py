import os
import sys
import json
import logging
from oaisdk import OaiSDK
from chat import ChatResource

# question = "What is ChatGPT?"
question = " ".join(sys.argv[1:])
print(f"{question}")
print("\n---\n")

# OaiSDK.setLogLevel(logging.DEBUG)

OaiSDK.auth(open(f"._osecret", "r").readlines()[0].strip())

def show_chat(chat):
    if not chat.response_ok():
        print(f"{chat.response_data}")
    else:
        answers = chat.data.answers
        n_answers = len(answers)

        for ii in range(n_answers):
            print(f"Answer {ii + 1}:")
            print(f"{answers[ii]}")
            print("\n---\n")

        print(f"{len(answers)} answer{'s' if n_answers > 1 else ''} were given by ChatGPT 3.5:")

chat = OaiSDK.resource('chat')
chat.ask(question, model="gpt-3.5-turbo")
show_chat(chat)
