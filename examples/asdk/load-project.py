from asdk import aSDK

# import logging
# aSDK.setLogLevel(logging.DEBUG)

aSDK.auth(open(f"._asecret", "r").readlines()[0].strip())

project = aSDK.resource("project")
project_list = project._list()
if not project.response_ok():
    print(project.response_data)
    exit(1)

this_project_gid = ""
for _ in project_list:
    if _["name"] == "Asana":
        this_project_gid = _["gid"]
        break
project.gid = this_project_gid

resp = project._load()
# print(resp)
print(project.request_http_method)
print(project.request)
print(project.response)
print(project.response_data)
# print(project)
