

from ..utils import Object


class MessageForwardOrigin(Object):
    """
    Contains information about the origin of a forwarded message

    No parameters required.
    """
    ID = "messageForwardOrigin"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "MessageForwardOriginUser or MessageForwardOriginHiddenUser or MessageForwardOriginChannel":
        if q.get("@type"):
            return Object.read(q)
        return MessageForwardOrigin()
