

from ..utils import Object


class InputMessageContent(Object):
    """
    The content of a message to send

    No parameters required.
    """
    ID = "inputMessageContent"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputMessageVideoNote or InputMessageLocation or InputMessageForwarded or InputMessageAudio or InputMessageSticker or InputMessageVoiceNote or InputMessagePoll or InputMessageGame or InputMessageAnimation or InputMessageDocument or InputMessageContact or InputMessageVideo or InputMessagePhoto or InputMessageText or InputMessageInvoice or InputMessageVenue":
        if q.get("@type"):
            return Object.read(q)
        return InputMessageContent()
