import os
from asdk import aSDK

# aSDK.setLogLevel(logging.DEBUG)

aSDK.auth(open(f"._asecret", "r").readlines()[0].strip())

project = aSDK.resource("project")
project_list = project._list()
print("\nAll projects")
for _ in project_list:
    print(f"\t{_['name']}")
print("")

project_id = project_list[-1]["gid"]
project_name = project_list[-1]["name"]
print(f"The last project is {project_name} ({project_id})")
project._load(project_id)
# print(project)

task = aSDK.resource("task")
task_list = task._list(project=project_id)
task_list.sort(key=lambda _: _["name"])
print(f"\nTasks of {project_name}")
for _ in task_list:
    print(f"\t{_['name']}")
print("")

user = aSDK.resource("user", gid="me")
user._load()
print(f"My user ID is {user.gid}")
print(user)
