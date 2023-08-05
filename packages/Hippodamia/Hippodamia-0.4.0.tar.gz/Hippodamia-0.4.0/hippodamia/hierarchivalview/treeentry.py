from hippodamia.enums import ViewDetails

"""
[ROOT]
  ├─ [ANode]
  │    ├─ [BNode]
  │    ├─ [CNode]
  │    │    ├─ [DNode]
  │    │    │    ├─ [ENode]
  │    │    │    └─ [FNode]
  │    │    └─ [GNode]
  │    └─ [HNode]
  └─ [INode]
       ├─ [JNode]
       ├─ [KNode]
       │    ├─ [LNode]
       │    └─ [MNode]
       └─ [NNode]


Root-ANode - prefix_first_line =  "  ├─ "
Root-ANode - prefix_next_lines =  "  │  "
ANode-CNode - prefix_first_line = "  │    ├─ "
ANode-CNode - prefix_next_lines = "  │    │  "
CNode-DNode - prefix_first_line = "  │    │    ├─ "
CNode-DNode - prefix_next_lines = "  │    │    │  "
INode-KNode - prefix_first_line = "       ├─ "
INode-KNode - prefix_next_lines = "       │  "

TYPE_A = "  ├─ "
TYPE_B = "  │  "
TYPE_C = "  └─ "
TYPE_D = "     "
"""


class Entry:
    MAX_NAME_LEN = 25
    INDENT = 2

    HORIZONTAL = "│"
    HORIZONTAL_CONNECTOR = "├"
    VERTICAL = "─"
    VERTICAL_CONNECTOR = "┬"
    EDGE = "└"
    SPACE = " "

    TYPE_A = SPACE + SPACE + HORIZONTAL_CONNECTOR + VERTICAL + SPACE
    TYPE_B = SPACE + SPACE + HORIZONTAL + SPACE + SPACE
    TYPE_C = SPACE + SPACE + EDGE + VERTICAL + SPACE
    TYPE_D = SPACE + SPACE + SPACE + SPACE + SPACE

    health = None
    name = None

    def __init__(self, name):
        if name is None or len(name) == 0:
            raise ValueError("Entry.__init__ - name must be set")
        self.name = name

    def update(self):
        raise NotImplementedError

    def _name2str(self):
        result = self.name
        if len(result) > self.MAX_NAME_LEN:
            result = result[:self.MAX_NAME_LEN - 3]
        result = "[{}]".format(result)
        return result

    def pformat(self, details=ViewDetails.NONE, filters=None):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError
