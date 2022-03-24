wiz = framework.model("wiz")

branch = framework.request.segment.branch
if branch is None: branch = wiz.workspace.branch()

kwargs['IS_DEV'] = wiz.is_dev()
kwargs['author'] = wiz.workspace.author(branch)
kwargs['BRANCH'] = branch
kwargs['BRANCHES'] = wiz.workspace.branches()
kwargs['TARGET_BRANCH'] = branch