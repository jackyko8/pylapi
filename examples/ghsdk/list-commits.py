from ghsdk import GhSDK

# import logging
# GhSDK.setLogLevel(logging.DEBUG)

GhSDK.auth(open(f"._gsecret", "r").readlines()[0].strip())

repo = GhSDK.resource("repo")
commit_list = repo.reposListCommits(owner="jackyko8", repo="pylapi")

if repo.response_ok():
    for commit in commit_list:
        print(f'----- {commit["sha"][0:6]}: {commit["commit"]["message"]}')
