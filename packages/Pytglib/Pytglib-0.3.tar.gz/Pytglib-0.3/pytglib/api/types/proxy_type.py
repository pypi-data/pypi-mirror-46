

from ..utils import Object


class ProxyType(Object):
    """
    Describes the type of the proxy server

    No parameters required.
    """
    ID = "proxyType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ProxyTypeSocks5 or ProxyTypeMtproto or ProxyTypeHttp":
        if q.get("@type"):
            return Object.read(q)
        return ProxyType()
