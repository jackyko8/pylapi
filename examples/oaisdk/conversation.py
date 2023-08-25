import os
import sys
import json
import logging
from oaisdk import OaiSDK
from chat import ChatResource

assistant_name = "ChatGPT 3.5"
exit_message = "bye"

# OaiSDK.setLogLevel(logging.DEBUG)
OaiSDK.auth(open(f"._osecret", "r").readlines()[0].strip())
chat = OaiSDK.resource("chat")

print(f"Welcome to {assistant_name} conversation app!")
print(f'To exit, please say "{exit_message}" when prompted for a message.')
print()
message_text = input("Instructions to the assistant, or press Enter to skip: ")
if message_text:
    chat.instruct_model(message_text)

while message_text.lower() != exit_message:
    print()
    message_text = input("Message: ")
    chat.ask(message_text)
    if not chat.response_ok():
        print(f"Sorry, there is an error: {chat.response_data}")
    else:
        answers = chat.data.answers
        n_answers = len(answers)
        if n_answers == 0:
            print(f"Sorry, {assistant_name} does not give any answers.")
        else:
            print(f"Reply:   {answers[0]}")
            if n_answers > 1:
                print(f"         (There are {n_answers} answers actually.)")

print("---")
print("Here is a recap of the conversation:")
print(json.dumps(chat._messages, indent=4))
