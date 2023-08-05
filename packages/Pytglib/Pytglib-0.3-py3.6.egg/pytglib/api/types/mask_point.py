

from ..utils import Object


class MaskPoint(Object):
    """
    Part of the face, relative to which a mask should be placed

    No parameters required.
    """
    ID = "maskPoint"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "MaskPointForehead or MaskPointChin or MaskPointEyes or MaskPointMouth":
        if q.get("@type"):
            return Object.read(q)
        return MaskPoint()
