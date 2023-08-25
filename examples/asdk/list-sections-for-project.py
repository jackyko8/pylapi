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

that_project_gid = ""
for _ in project_list:
    if _["name"] == "Personal":
        that_project_gid = _["gid"]
        break

# Option keyword
print("---------- Keyword: ")
try:
    section_list = project.getSectionsForProject(gid=that_project_gid)
    print(section_list)
except:
    print("Failed")

# Option positional
print("---------- Position: ")
try:
    section_list = project.getSectionsForProject(that_project_gid)
    print(section_list)
except:
    print("Failed")

# Option implicit
print("---------- Implicit: ")
try:
    section_list = project.getSectionsForProject()
    print(section_list)
except:
    print("Failed")

# print(section_list)
# for x in section_list:
#     print(f"{x['name']} ({x['gid']})")
# print("")
