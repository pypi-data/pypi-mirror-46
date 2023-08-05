

from ..utils import Object


class SearchMessagesFilter(Object):
    """
    Represents a filter for message search results

    No parameters required.
    """
    ID = "searchMessagesFilter"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "SearchMessagesFilterMention or SearchMessagesFilterAnimation or SearchMessagesFilterVoiceAndVideoNote or SearchMessagesFilterEmpty or SearchMessagesFilterVideoNote or SearchMessagesFilterDocument or SearchMessagesFilterAudio or SearchMessagesFilterPhotoAndVideo or SearchMessagesFilterChatPhoto or SearchMessagesFilterVideo or SearchMessagesFilterUrl or SearchMessagesFilterMissedCall or SearchMessagesFilterVoiceNote or SearchMessagesFilterUnreadMention or SearchMessagesFilterCall or SearchMessagesFilterPhoto":
        if q.get("@type"):
            return Object.read(q)
        return SearchMessagesFilter()
