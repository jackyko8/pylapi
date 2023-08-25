from asdk import aSDK

# import logging
# aSDK.setLogLevel(logging.DEBUG)

aSDK.auth(open(f"._asecret", "r").readlines()[0].strip())

tag = aSDK.resource('tag')
tag_list = tag._list()
print(tag_list)
for _ in tag_list:
    print(f"{_['name']}")
print("")
