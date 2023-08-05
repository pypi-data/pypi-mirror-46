from collections import deque
from hippodamia.hierarchivalview.treeroot import Root
from hippodamia.hierarchivalview.treeleaf import Leaf
from hippodamia.enums import ViewDetails
from threading import Lock
from pelops.logging.mylogger import get_child


class HierarchicalView:
    _logger = None
    _agentshadows = None

    tree = None
    _tree_lock = None

    def __init__(self, agentshadows, logger):
        self._logger = get_child(logger, self.__class__.__name__)
        self._logger.info("__init__")
        self._agentshadows = agentshadows
        self._tree_lock = Lock()
        self._update_tree()
        self._logger.debug("__init__ - finished")

    def _update_tree(self):
        self._logger.debug("_update_tree")
        self._build_tree()
        self._logger.debug("_update_tree - updating info within tree")
        self.tree.update()

    def pformat(self, details=ViewDetails.HEALTH, filters=None):
        self._logger.debug("pformat - waiting for lock")
        with self._tree_lock:
            self._update_tree()
            if filters is None:
                filters = deque([None, None, None, None])
            else:
                filters = deque([filters["LOCATION"], filters["ROOM"], filters["DEVICE"], filters["SERVICE"]])
            result = self.tree.pformat(details, filters)
            self._logger.info("pformat success")
            return result

    def to_dict(self):
        self._logger.debug("to_dict - waiting for lock")
        with self._tree_lock:
            self._update_tree()
            result = self.tree.to_dict()
            self._logger.info("to_dict success")
            return result

    def _build_tree(self):
        self._logger.debug("_build_tree - start")
        leafs = {}
        for gid, shadow in self._agentshadows.items():
            try:
                leafs[gid] = Leaf(shadow)
                self._logger.debug("_build_tree - added gid {}".format(gid))
            except ValueError:
                self._logger.debug("_build_tree - skipped gid {}".format(gid))
                pass
        self._logger.debug("_build_tree - creating root node with leafs {}".format(leafs))
        self.tree = Root(leafs)
        self._logger.debug("_build_tree - finish")

    def start(self):
        pass

    def stop(self):
        pass
