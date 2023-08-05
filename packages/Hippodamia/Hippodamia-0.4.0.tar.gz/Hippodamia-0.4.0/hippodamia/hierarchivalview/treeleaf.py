from hippodamia.hierarchivalview.treeentry import Entry
from hippodamia.enums import ViewDetails
from hippodamia.enums import Health
from hippodamia.enums import Necessity
from collections import deque


class Leaf(Entry):
    gid = None
    shadow = None
    breadcrumbs = None

    def __init__(self, shadow):
        Entry.__init__(self, shadow.properties.name)
        self.shadow = shadow
        self.gid = self.shadow.properties.gid
        self.breadcrumbs = deque()
        self.update()

    def update(self):
        self.health = self.shadow.properties.health
        self.name = self.shadow.properties.name
        self.breadcrumbs = deque([self.shadow.properties.location, self.shadow.properties.room,
                                  self.shadow.properties.device])
        result = self.health
        if self.shadow.properties.necessity != Necessity.REQUIRED:
            result = min(result, Health.YELLOW)
        return result

    def get_state(self):
        return self.shadow.get_state_id().name

    def get_health(self):
        return self.health.name

    def pformat(self, details=ViewDetails.NONE, filters=None):
        result = [self._name2str()]

        if details & ViewDetails.HEALTH == ViewDetails.HEALTH:
            result.append(self.get_health())
        if details & ViewDetails.STATE == ViewDetails.STATE:
            result.append(self.get_state())
        if details & ViewDetails.GID == ViewDetails.GID:
            result.append("gid:")
            result.append(self.gid)

        result = " ".join(result)
        return result

    def to_dict(self):
        result = {
            "type": self.__class__.__name__,
            "name": self._name2str(),
            "health": self.get_health(),
            "state": self.get_state(),
            "gid": self.gid
        }
        return result
