

from ..utils import Object


class NotificationGroupType(Object):
    """
    Describes type of notifications in the group

    No parameters required.
    """
    ID = "notificationGroupType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "NotificationGroupTypeSecretChat or NotificationGroupTypeMentions or NotificationGroupTypeCalls or NotificationGroupTypeMessages":
        if q.get("@type"):
            return Object.read(q)
        return NotificationGroupType()
