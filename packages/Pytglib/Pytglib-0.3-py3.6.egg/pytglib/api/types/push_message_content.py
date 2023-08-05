

from ..utils import Object


class PushMessageContent(Object):
    """
    Contains content of a push message notification

    No parameters required.
    """
    ID = "pushMessageContent"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PushMessageContentVoiceNote or PushMessageContentInvoice or PushMessageContentGameScore or PushMessageContentAnimation or PushMessageContentMediaAlbum or PushMessageContentAudio or PushMessageContentContactRegistered or PushMessageContentChatChangeTitle or PushMessageContentChatJoinByLink or PushMessageContentDocument or PushMessageContentHidden or PushMessageContentVideoNote or PushMessageContentBasicGroupChatCreate or PushMessageContentText or PushMessageContentSticker or PushMessageContentChatDeleteMember or PushMessageContentContact or PushMessageContentLocation or PushMessageContentVideo or PushMessageContentGame or PushMessageContentPoll or PushMessageContentChatAddMembers or PushMessageContentChatChangePhoto or PushMessageContentScreenshotTaken or PushMessageContentPhoto or PushMessageContentMessageForwards":
        if q.get("@type"):
            return Object.read(q)
        return PushMessageContent()
