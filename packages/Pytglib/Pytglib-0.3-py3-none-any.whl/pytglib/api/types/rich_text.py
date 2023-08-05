

from ..utils import Object


class RichText(Object):
    """
    Describes a text object inside an instant-view web page

    No parameters required.
    """
    ID = "richText"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "RichTextFixed or RichTextPhoneNumber or RichTextIcon or RichTextUrl or RichTextItalic or RichTextPlain or RichTextEmailAddress or RichTextMarked or RichTextStrikethrough or RichTextSubscript or RichTextSuperscript or RichTextAnchor or RichTextUnderline or RichTextBold or RichTexts":
        if q.get("@type"):
            return Object.read(q)
        return RichText()
