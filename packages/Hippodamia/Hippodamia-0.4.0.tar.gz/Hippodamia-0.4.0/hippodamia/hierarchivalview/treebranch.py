from hippodamia.hierarchivalview.treeentry import Entry
from hippodamia.hierarchivalview.treeleaf import Leaf
from hippodamia.enums import ViewDetails
from hippodamia.enums import Health
from collections import deque


class Branch(Entry):
    children = None

    def __init__(self, name):
        Entry.__init__(self, name)
        self.children = {}
        self.update()

    def update(self, children=None):
        if children is None:
            children = self.children

        self.health = Health.GREEN
        for gid, leaf in children.items():
            leaf_health = leaf.update()
            self.health = max(self.health, leaf_health)

        return self.health

    def add_leaf(self, leaf, breadcrumbs, children=None):
        if children is None:
            children = self.children

        if len(breadcrumbs) == 0:
            children[leaf.gid] = leaf
        else:
            branch_name = breadcrumbs.popleft()
            if branch_name is None or branch_name == "":
                branch_name = "_"

            if branch_name not in children:
                children[branch_name] = Branch(branch_name)
            children[branch_name].add_leaf(leaf, breadcrumbs)

    def pformat(self, details=ViewDetails.NONE, filters=None):
        if filters is None:
            filters = deque()
        lines = self.tree_view("", "", details, filters)
        result = "\n".join(lines)
        return  result

    @staticmethod
    def _filter_match(name, entry_filter):
        if entry_filter is not None:
            name = name.lower()
            entry_filter = entry_filter.lower()
            return name.startswith(entry_filter)
        return True

    def tree_view(self, prefix_first_line, prefix_next_lines, details, filters):
        filters = filters.copy()
        try:
            entry_filter = filters.popleft()
        except IndexError:
            entry_filter = None

        first_line = prefix_first_line + self._pprint_details(details)
        lines = [first_line]
        prefix_a = prefix_next_lines + self.TYPE_A
        prefix_b = prefix_next_lines + self.TYPE_B
        prefix_c = prefix_next_lines + self.TYPE_C
        prefix_d = prefix_next_lines + self.TYPE_D

        counter = 0
        for name, entry in self.children.items():
            counter += 1
            if self._filter_match(name, entry_filter):
                if counter == len(self.children):
                    # last entry
                    prefix_first = prefix_c
                    prefix_next = prefix_d
                else:
                    prefix_first = prefix_a
                    prefix_next = prefix_b

                if type(entry) is Leaf:
                    line = prefix_first + entry.pformat(details)
                    lines.append(line)
                elif type(entry) is Branch:
                    sub_lines = entry.tree_view(prefix_first, prefix_next, details, filters)
                    lines += sub_lines
                else:
                    raise TypeError

        return lines

    def _pprint_details(self, details):
        result = [self._name2str()]
        if details & ViewDetails.HEALTH == ViewDetails.HEALTH:
            result.append(self.health.name)
        if details & ViewDetails.STATE == ViewDetails.STATE:
            pass
        if details & ViewDetails.GID == ViewDetails.GID:
            pass
        result = " ".join(result)
        return result

    def to_dict(self):
        result = {
            "type": self.__class__.__name__,
            "name": self._name2str(),
            "health": self.health.name,
            "state": None,
            "gid": None,
            "children": []
        }
        for child in self.children.values():
            result["children"].append(child.to_dict())
        return result
