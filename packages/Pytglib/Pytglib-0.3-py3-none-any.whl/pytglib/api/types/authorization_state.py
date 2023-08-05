

from ..utils import Object


class AuthorizationState(Object):
    """
    Represents the current authorization state of the client

    No parameters required.
    """
    ID = "authorizationState"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "AuthorizationStateWaitPhoneNumber or AuthorizationStateClosing or AuthorizationStateWaitEncryptionKey or AuthorizationStateReady or AuthorizationStateWaitTdlibParameters or AuthorizationStateWaitPassword or AuthorizationStateClosed or AuthorizationStateLoggingOut or AuthorizationStateWaitCode":
        if q.get("@type"):
            return Object.read(q)
        return AuthorizationState()
