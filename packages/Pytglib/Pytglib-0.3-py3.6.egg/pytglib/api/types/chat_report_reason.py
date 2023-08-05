

from ..utils import Object


class ChatReportReason(Object):
    """
    Describes the reason why a chat is reported

    No parameters required.
    """
    ID = "chatReportReason"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatReportReasonViolence or ChatReportReasonChildAbuse or ChatReportReasonPornography or ChatReportReasonCopyright or ChatReportReasonSpam or ChatReportReasonCustom":
        if q.get("@type"):
            return Object.read(q)
        return ChatReportReason()
