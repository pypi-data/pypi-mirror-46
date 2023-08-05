

from ..utils import Object


class PassportElementType(Object):
    """
    Contains the type of a Telegram Passport element

    No parameters required.
    """
    ID = "passportElementType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PassportElementTypeUtilityBill or PassportElementTypeRentalAgreement or PassportElementTypePersonalDetails or PassportElementTypePhoneNumber or PassportElementTypePassport or PassportElementTypeBankStatement or PassportElementTypePassportRegistration or PassportElementTypeAddress or PassportElementTypeDriverLicense or PassportElementTypeTemporaryRegistration or PassportElementTypeIdentityCard or PassportElementTypeEmailAddress or PassportElementTypeInternalPassport":
        if q.get("@type"):
            return Object.read(q)
        return PassportElementType()
