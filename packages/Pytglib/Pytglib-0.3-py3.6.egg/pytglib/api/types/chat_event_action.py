

from ..utils import Object


class ChatEventAction(Object):
    """
    Represents a chat event

    No parameters required.
    """
    ID = "chatEventAction"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatEventMemberJoined or ChatEventTitleChanged or ChatEventMemberLeft or ChatEventMessageDeleted or ChatEventSignMessagesToggled or ChatEventMessageUnpinned or ChatEventMemberPromoted or ChatEventMemberInvited or ChatEventUsernameChanged or ChatEventMemberRestricted or ChatEventMessagePinned or ChatEventDescriptionChanged or ChatEventMessageEdited or ChatEventInvitesToggled or ChatEventStickerSetChanged or ChatEventPhotoChanged or ChatEventIsAllHistoryAvailableToggled":
        if q.get("@type"):
            return Object.read(q)
        return ChatEventAction()
