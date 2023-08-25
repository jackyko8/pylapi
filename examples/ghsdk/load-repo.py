from ghsdk import GhSDK

# import logging
# GhSDK.setLogLevel(logging.DEBUG)

GhSDK.auth(open(f"._gsecret", "r").readlines()[0].strip())

user = GhSDK.resource("user")
repo_list = user.reposListForAuthenticatedUser()
for _ in repo_list: print(f"{_['name']} by {_['owner']['login']}")
owner = repo_list[0]["owner"]["login"]
repo_name = repo_list[0]["name"]
print()
print(owner)
print(repo_name)

repo = GhSDK.resource("repo")
repo.data = repo.reposGet(owner=owner, repo=repo_name)
print(repo)

# import os
# import logging
# from gpylapi import GPyLapi

# # GPyLapi.setLogLevel(logging.DEBUG)

# GPyLapi.auth(os.environ["GHSDK_AUTH"])

# repo = GPyLapi.resource('repo')
# print(repo)

# repo_owner = "jackyko8"
# repo_repo = "pylapi"
# repo_path = "README.md"

# repo.owner = repo_owner
# repo.repo = repo_repo
# repo.path = repo_path
# print(repo)

# print(repo.owner)
# print(repo.repo)
# # print(repo.path)

# # del repo.owner
# print(repo)

# repo.load()
# if repo.response_ok():
#     print(repo)

# # repo_list = repo.list()
# # print(repo_list)

# print(repo.request_http_method)
# print(repo.request)
# print(repo.response)
# print(repo.response_data)
