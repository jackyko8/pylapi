from ghsdk import GhSDK

# import logging
# GhSDK.setLogLevel(logging.DEBUG)

GhSDK.auth(open(f"._gsecret", "r").readlines()[0].strip())

repo = GhSDK.resource("repo")
branch_list = repo.reposListBranches(owner="jackyko8", repo="pylapi")

if repo.response_ok():
    for _ in branch_list: print(_["name"])
