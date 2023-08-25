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

user = aSDK.resource('user')
user_list = user._list()
print(f"user_list = {user_list}")
user.data = user_list[0]
# user._load()
print(f"{user}")

task = aSDK.resource('task')
task.data.name = "Test Task 4"
task.data.workspace = workspace.gid
task.data.assignee = user.gid
print(task)

# resp = task._create(data=task.data.to_data(), workspace=workspace.gid, assignee=user.gid)
resp = task._create(data=task.data.to_data())
print(resp)
print(task.request_http_method)
print(task.request)
print(task.response)
print(task.response_data)
print(task)
