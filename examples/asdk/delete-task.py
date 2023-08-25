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
user_task_list = aSDK.resource("user_task_list")
user_task_list.data = user.getUserTaskListForUser(gid="me", workspace=workspace.gid)
print(user_task_list)

utl = user_task_list.getTasksForUserTaskList()
print(f"{len(utl)} tasks in utl")

task = aSDK.resource('task')
for _ in utl:
    if _["name"] == "Test Task 4":
        task.data = _
        break
print(task)

resp = task._delete()
print(resp)
print(task.request_http_method)
print(task.request)
print(task.response)
print(task.response_data)
print(task)
