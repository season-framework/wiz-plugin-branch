wiz = framework.model("wiz")

merge = wiz.workspace.merge()
active_branches = merge.branches()
branch = framework.request.segment.branch
base_branch = framework.request.segment.base_branch
active_branches = [h['from'] + "_" + h['to'] for h in active_branches]
merge_path = branch + "_" + base_branch

if merge_path not in active_branches:
    framework.response.redirect("/wiz/admin/branch")

merge.checkout(branch, base_branch)
author = merge.author()

kwargs['IS_DEV'] = wiz.is_dev()
kwargs['author'] = author
kwargs['BRANCH'] = branch
kwargs['BRANCHES'] = wiz.workspace.branches()
kwargs['TARGET_BRANCH'] = merge_path