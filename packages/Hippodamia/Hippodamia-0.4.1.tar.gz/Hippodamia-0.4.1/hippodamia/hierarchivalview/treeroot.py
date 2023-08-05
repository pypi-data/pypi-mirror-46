from hippodamia.hierarchivalview.treebranch import Branch


class Root(Branch):
    def __init__(self, leafs):
        Branch.__init__(self, name="__root__")
        self._build_tree(leafs)

    def _build_tree(self, leafs):
        new_children = {}

        for gid, leaf in leafs.items():
            breadcrumbs = leaf.breadcrumbs.copy()
            self.add_leaf(leaf, breadcrumbs, new_children)

        self.children = new_children
        self.update()

    def to_dict(self):
        result = Branch.to_dict(self)
        result["type"] = Branch.__name__
        return result
