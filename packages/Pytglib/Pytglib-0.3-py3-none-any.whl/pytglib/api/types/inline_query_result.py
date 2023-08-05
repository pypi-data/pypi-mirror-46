

from ..utils import Object


class InlineQueryResult(Object):
    """
    Represents a single result of an inline query

    No parameters required.
    """
    ID = "inlineQueryResult"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InlineQueryResultAudio or InlineQueryResultVoiceNote or InlineQueryResultVenue or InlineQueryResultArticle or InlineQueryResultVideo or InlineQueryResultDocument or InlineQueryResultContact or InlineQueryResultGame or InlineQueryResultLocation or InlineQueryResultPhoto or InlineQueryResultSticker or InlineQueryResultAnimation":
        if q.get("@type"):
            return Object.read(q)
        return InlineQueryResult()
