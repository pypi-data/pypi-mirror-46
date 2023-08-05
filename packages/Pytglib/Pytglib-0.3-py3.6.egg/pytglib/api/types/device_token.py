

from ..utils import Object


class DeviceToken(Object):
    """
    Represents a data needed to subscribe for push notifications through registerDevice method. To use specific push notification service, you must specify the correct application platform and upload valid server authentication data at https://my.telegram.org

    No parameters required.
    """
    ID = "deviceToken"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "DeviceTokenSimplePush or DeviceTokenMicrosoftPushVoIP or DeviceTokenUbuntuPush or DeviceTokenWebPush or DeviceTokenTizenPush or DeviceTokenApplePushVoIP or DeviceTokenApplePush or DeviceTokenBlackBerryPush or DeviceTokenMicrosoftPush or DeviceTokenFirebaseCloudMessaging or DeviceTokenWindowsPush":
        if q.get("@type"):
            return Object.read(q)
        return DeviceToken()
