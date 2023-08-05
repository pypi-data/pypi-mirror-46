

from ..utils import Object


class MessageContent(Object):
    """
    Contains the content of a message

    No parameters required.
    """
    ID = "messageContent"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "MessagePinMessage or MessageWebsiteConnected or MessageChatUpgradeFrom or MessageExpiredPhoto or MessageChatJoinByLink or MessageGameScore or MessagePaymentSuccessful or MessageCall or MessageChatChangeTitle or MessagePoll or MessageContactRegistered or MessageChatChangePhoto or MessageSticker or MessageChatUpgradeTo or MessageDocument or MessageVideoNote or MessageChatSetTtl or MessagePhoto or MessageContact or MessagePassportDataReceived or MessageChatDeleteMember or MessageVenue or MessageText or MessageChatDeletePhoto or MessageExpiredVideo or MessageSupergroupChatCreate or MessageAudio or MessageScreenshotTaken or MessageLocation or MessageChatAddMembers or MessageVideo or MessagePaymentSuccessfulBot or MessageUnsupported or MessageVoiceNote or MessageAnimation or MessageCustomServiceAction or MessageBasicGroupChatCreate or MessageInvoice or MessageGame or MessagePassportDataSent":
        if q.get("@type"):
            return Object.read(q)
        return MessageContent()
