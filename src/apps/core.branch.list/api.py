import season
import json
from werkzeug.exceptions import HTTPException

wiz = framework.model("wiz")

def create(framework):
    branch = framework.request.query("branch", True)
    base = framework.request.query("base_branch", "master")

    allowed = "qwertyuiopasdfghjklzxcvbnm-1234567890"
    for ns in branch:
        if ns not in allowed:
            raise Exception(f"only alphabet and number and -, _ in branch name")
    for ns in base:
        if ns not in allowed:
            raise Exception(f"only alphabet and number and -, _ in branch name")

    blocked = ['copy', 'ref', 'commit', 'branch', 'delete', 'cache']
    if branch in blocked:
        raise Exception(f"blocked keyword `{branch}` for branch name")

    name = framework.request.query("name", None)
    email = framework.request.query("email", None)

    wiz.workspace.checkout(branch=branch, base_branch=base, name=name, email=email, reload=True)
    framework.response.cookies.set("season-wiz-branch", branch)
    framework.response.status(200, True)

def delete(framework):
    branch = framework.request.query("branch", True)
    remote = framework.request.query("remote", True)
    if remote == 'true': remote = True
    else: remote = False
    wiz.workspace.delete(branch, remote)
    framework.response.status(200, True)

def list(framework):
    branches = wiz.workspace.branches(working=True, git=True, status=True)
    active_branch = []
    stale_branch = []
    
    for i in range(len(branches)):
        if branches[i]['working']:
            try:
                branches[i]['changed'] = wiz.workspace.changed(branches[i]['name'])
            except:
                pass
            try:
                branches[i]['author'] = wiz.workspace.author(branches[i]['name'])
            except:
                pass
            active_branch.append(branches[i])
        else:
            stale_branch.append(branches[i])
        
    merge = wiz.workspace.merge()
    pull_request = merge.branches()
    for i in range(len(pull_request)):
        try:
            merge.checkout(pull_request[i]['from'], pull_request[i]['to'])
            pull_request[i]['author'] = merge.author()
        except:
            pass
    
    framework.response.status(200, active=active_branch, stale=stale_branch, pull_request=pull_request)

def pull_request(framework):
    branch = framework.request.query("branch", True)
    base = framework.request.query("base_branch", True)
    name = framework.request.query("name", None)
    email = framework.request.query("email", None)

    fs = framework.model("wizfs").use(f"wiz/merge")
    if fs.isdir(f"{branch}_{base}"):
        framework.response.status(500, "merge request on working. please delete previous work.")    

    # branch: source branch, base_branch: apply changed
    wiz.workspace.merge().checkout(branch, base, name=name, email=email)

    framework.response.status(200, True)

def delete_request(framework):
    branch = framework.request.query("branch", True)
    base = framework.request.query("base_branch", True)
    merge = wiz.workspace.merge().checkout(branch, base)
    merge.delete()
    framework.response.status(200, True)