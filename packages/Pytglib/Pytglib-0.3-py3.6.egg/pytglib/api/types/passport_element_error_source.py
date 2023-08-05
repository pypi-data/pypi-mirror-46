

from ..utils import Object


class PassportElementErrorSource(Object):
    """
    Contains the description of an error in a Telegram Passport element

    No parameters required.
    """
    ID = "passportElementErrorSource"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PassportElementErrorSourceSelfie or PassportElementErrorSourceFile or PassportElementErrorSourceDataField or PassportElementErrorSourceFiles or PassportElementErrorSourceUnspecified or PassportElementErrorSourceTranslationFiles or PassportElementErrorSourceTranslationFile or PassportElementErrorSourceFrontSide or PassportElementErrorSourceReverseSide":
        if q.get("@type"):
            return Object.read(q)
        return PassportElementErrorSource()
