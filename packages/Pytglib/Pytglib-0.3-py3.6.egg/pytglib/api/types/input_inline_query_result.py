

from ..utils import Object


class InputInlineQueryResult(Object):
    """
    Represents a single result of an inline query; for bots only

    No parameters required.
    """
    ID = "inputInlineQueryResult"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputInlineQueryResultContact or InputInlineQueryResultPhoto or InputInlineQueryResultAnimatedMpeg4 or InputInlineQueryResultVideo or InputInlineQueryResultVoiceNote or InputInlineQueryResultAnimatedGif or InputInlineQueryResultVenue or InputInlineQueryResultArticle or InputInlineQueryResultGame or InputInlineQueryResultSticker or InputInlineQueryResultAudio or InputInlineQueryResultDocument or InputInlineQueryResultLocation":
        if q.get("@type"):
            return Object.read(q)
        return InputInlineQueryResult()
