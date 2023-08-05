

from ..utils import Object


class InlineKeyboardButtonType(Object):
    """
    Describes the type of an inline keyboard button

    No parameters required.
    """
    ID = "inlineKeyboardButtonType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InlineKeyboardButtonTypeSwitchInline or InlineKeyboardButtonTypeCallback or InlineKeyboardButtonTypeCallbackGame or InlineKeyboardButtonTypeBuy or InlineKeyboardButtonTypeUrl":
        if q.get("@type"):
            return Object.read(q)
        return InlineKeyboardButtonType()
