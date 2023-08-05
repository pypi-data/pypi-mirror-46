

from ..utils import Object


class InputPassportElementErrorSource(Object):
    """
    Contains the description of an error in a Telegram Passport element; for bots only

    No parameters required.
    """
    ID = "inputPassportElementErrorSource"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputPassportElementErrorSourceTranslationFile or InputPassportElementErrorSourceFrontSide or InputPassportElementErrorSourceDataField or InputPassportElementErrorSourceFiles or InputPassportElementErrorSourceReverseSide or InputPassportElementErrorSourceFile or InputPassportElementErrorSourceUnspecified or InputPassportElementErrorSourceTranslationFiles or InputPassportElementErrorSourceSelfie":
        if q.get("@type"):
            return Object.read(q)
        return InputPassportElementErrorSource()
