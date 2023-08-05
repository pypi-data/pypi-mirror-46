

from ..utils import Object


class PassportElement(Object):
    """
    Contains information about a Telegram Passport element

    No parameters required.
    """
    ID = "passportElement"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PassportElementPhoneNumber or PassportElementEmailAddress or PassportElementIdentityCard or PassportElementPassportRegistration or PassportElementRentalAgreement or PassportElementPassport or PassportElementPersonalDetails or PassportElementTemporaryRegistration or PassportElementDriverLicense or PassportElementInternalPassport or PassportElementUtilityBill or PassportElementAddress or PassportElementBankStatement":
        if q.get("@type"):
            return Object.read(q)
        return PassportElement()
