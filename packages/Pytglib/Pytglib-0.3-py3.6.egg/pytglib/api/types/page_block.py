

from ..utils import Object


class PageBlock(Object):
    """
    Describes a block of an instant view web page

    No parameters required.
    """
    ID = "pageBlock"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PageBlockRelatedArticles or PageBlockBlockQuote or PageBlockAudio or PageBlockCollage or PageBlockAnchor or PageBlockHeader or PageBlockDivider or PageBlockCover or PageBlockVideo or PageBlockSubtitle or PageBlockTable or PageBlockPullQuote or PageBlockDetails or PageBlockEmbedded or PageBlockAuthorDate or PageBlockSubheader or PageBlockParagraph or PageBlockAnimation or PageBlockEmbeddedPost or PageBlockChatLink or PageBlockKicker or PageBlockFooter or PageBlockTitle or PageBlockList or PageBlockMap or PageBlockPreformatted or PageBlockSlideshow or PageBlockPhoto":
        if q.get("@type"):
            return Object.read(q)
        return PageBlock()
