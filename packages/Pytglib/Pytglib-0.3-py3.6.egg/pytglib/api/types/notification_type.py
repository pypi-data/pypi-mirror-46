

from ..utils import Object


class NotificationType(Object):
    """
    Contains detailed information about a notification

    No parameters required.
    """
    ID = "notificationType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "NotificationTypeNewSecretChat or NotificationTypeNewMessage or NotificationTypeNewCall or NotificationTypeNewPushMessage":
        if q.get("@type"):
            return Object.read(q)
        return NotificationType()
