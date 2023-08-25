from asdk import aSDK

# import logging
# aSDK.setLogLevel(logging.DEBUG)

aSDK.auth(open(f"._asecret", "r").readlines()[0].strip())

def findProject(project_name, project):
    project_list = project._list()
    if not project.response_ok():
        print(project.response_data)
        exit(1)
    for _ in project_list:
        if _["name"] == project_name:
            project.data = _
            break
    return project

def findTask(task_name, project_gid, task):
    task_list = task._list(project=project_gid)
    if not task.response_ok():
        print(task.response_data)
        exit(1)
    for _ in task_list:
        if _["name"] == task_name:
            task.data = _
            break
    return task

project_target = aSDK.resource("project")
findProject("Asana", project_target)
print(project_target)

project_source = aSDK.resource("project")
findProject("Personal", project_source)
print(project_source)

task = aSDK.resource("task")
findTask("Test Task 2", project_source.gid, task)
print(task)

resp = task.addProjectForTask(data={"project": project_target.gid})
print(resp)
print(task.request_http_method)
print(task.request)
print(task.response)
print(task.response_data)
print(task)
