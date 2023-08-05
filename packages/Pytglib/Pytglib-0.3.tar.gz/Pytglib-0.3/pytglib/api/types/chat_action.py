

from ..utils import Object


class ChatAction(Object):
    """
    Describes the different types of activity in a chat

    No parameters required.
    """
    ID = "chatAction"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatActionUploadingVideoNote or ChatActionStartPlayingGame or ChatActionRecordingVideoNote or ChatActionUploadingVideo or ChatActionUploadingDocument or ChatActionRecordingVideo or ChatActionChoosingContact or ChatActionCancel or ChatActionChoosingLocation or ChatActionTyping or ChatActionRecordingVoiceNote or ChatActionUploadingPhoto or ChatActionUploadingVoiceNote":
        if q.get("@type"):
            return Object.read(q)
        return ChatAction()
