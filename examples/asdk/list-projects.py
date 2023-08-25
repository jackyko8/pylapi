from asdk import aSDK

# import logging
# aSDK.setLogLevel(logging.DEBUG)

aSDK.auth(open(f"._asecret", "r").readlines()[0].strip())

project = aSDK.resource("project")
project_list = project._list()
# print(project_list)
for _ in project_list:
    print(f"{_['name']}")
print("")
