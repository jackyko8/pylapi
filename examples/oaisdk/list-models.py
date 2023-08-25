import os
from oaisdk import OaiSDK
import json

# OPyLapi.setLogLevel(logging.DEBUG)

OaiSDK.auth(open(f"._osecret", "r").readlines()[0].strip())

model = OaiSDK.resource('model')
model_list = model.list()
if model.response_ok():
    # print(json.dumps(model_list, indent=4))
    # print(json.dumps(model_list[0], indent=4))
    model_id_list = [_["id"] for _ in model_list]
    model_id_list.sort()
    for _ in model_id_list: print(_)

# print(model.request_http_method)
# print(model.request)
# print(model.response.json())
# print(model.response_data)
