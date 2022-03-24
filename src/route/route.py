framework.layout('core.theme.layout', navbar=True, monaco=False)
framework.render("list", "core.branch.list")

framework.layout('core.theme.layout', navbar=False, monaco=True)
framework.render("commit/<branch>", "core.branch.commit")
framework.render("merge/<branch>/<base_branch>", "core.branch.merge")

framework.response.redirect("list")