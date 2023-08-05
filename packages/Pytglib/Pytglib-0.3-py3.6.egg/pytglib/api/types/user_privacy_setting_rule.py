

from ..utils import Object


class UserPrivacySettingRule(Object):
    """
    Represents a single rule for managing privacy settings

    No parameters required.
    """
    ID = "userPrivacySettingRule"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "UserPrivacySettingRuleAllowAll or UserPrivacySettingRuleRestrictContacts or UserPrivacySettingRuleRestrictUsers or UserPrivacySettingRuleRestrictAll or UserPrivacySettingRuleAllowContacts or UserPrivacySettingRuleAllowUsers":
        if q.get("@type"):
            return Object.read(q)
        return UserPrivacySettingRule()
