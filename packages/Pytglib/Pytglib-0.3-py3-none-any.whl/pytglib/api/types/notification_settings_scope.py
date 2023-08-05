

from ..utils import Object


class NotificationSettingsScope(Object):
    """
    Describes the types of chats to which notification settings are applied

    No parameters required.
    """
    ID = "notificationSettingsScope"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "NotificationSettingsScopeGroupChats or NotificationSettingsScopeChannelChats or NotificationSettingsScopePrivateChats":
        if q.get("@type"):
            return Object.read(q)
        return NotificationSettingsScope()
