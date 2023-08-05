

from ..utils import Object


class TextEntityType(Object):
    """
    Represents a part of the text which must be formatted differently

    No parameters required.
    """
    ID = "textEntityType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "TextEntityTypePre or TextEntityTypeHashtag or TextEntityTypeBotCommand or TextEntityTypeItalic or TextEntityTypePhoneNumber or TextEntityTypeCode or TextEntityTypePreCode or TextEntityTypeMention or TextEntityTypeMentionName or TextEntityTypeUrl or TextEntityTypeCashtag or TextEntityTypeBold or TextEntityTypeTextUrl or TextEntityTypeEmailAddress":
        if q.get("@type"):
            return Object.read(q)
        return TextEntityType()
