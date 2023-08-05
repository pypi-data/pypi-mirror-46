

from ..utils import Object


class InputPassportElement(Object):
    """
    Contains information about a Telegram Passport element to be saved

    No parameters required.
    """
    ID = "inputPassportElement"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputPassportElementPassport or InputPassportElementEmailAddress or InputPassportElementAddress or InputPassportElementRentalAgreement or InputPassportElementInternalPassport or InputPassportElementPassportRegistration or InputPassportElementPersonalDetails or InputPassportElementPhoneNumber or InputPassportElementBankStatement or InputPassportElementDriverLicense or InputPassportElementTemporaryRegistration or InputPassportElementIdentityCard or InputPassportElementUtilityBill":
        if q.get("@type"):
            return Object.read(q)
        return InputPassportElement()
