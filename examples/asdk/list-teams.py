from asdk import aSDK

# import logging
# aSDK.setLogLevel(logging.DEBUG)

aSDK.auth(open(f"._asecret", "r").readlines()[0].strip())

workspace = aSDK.resource('workspace')
workspace_list = workspace._list()
print(f"ws_list = {workspace_list}")
workspace.data = workspace_list[0]
# ws._load()
print(f"{workspace}")

team = aSDK.resource('team')
team_list = team._list(workspace=workspace.gid)
# print(team_list)
for _ in team_list:
    print(f"{_['name']}")
