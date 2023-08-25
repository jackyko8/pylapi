import os
from oaisdk import OaiSDK
import json

# OPyLapi.setLogLevel(logging.DEBUG)

OaiSDK.auth(open(f"._osecret", "r").readlines()[0].strip())

model_id = "gpt-3.5-turbo"
model = OaiSDK.resource('model')
model.load(model_id)
if model.response_ok():
    print(model)
    print(model.id)
# print(model.request_http_method)
# print(model.request)
# print(model.response)
# print(model.response_data)
# print(model.response.ok)
