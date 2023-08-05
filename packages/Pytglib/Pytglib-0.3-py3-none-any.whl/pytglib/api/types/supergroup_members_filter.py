

from ..utils import Object


class SupergroupMembersFilter(Object):
    """
    Specifies the kind of chat members to return in getSupergroupMembers

    No parameters required.
    """
    ID = "supergroupMembersFilter"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "SupergroupMembersFilterSearch or SupergroupMembersFilterBanned or SupergroupMembersFilterRecent or SupergroupMembersFilterAdministrators or SupergroupMembersFilterBots or SupergroupMembersFilterRestricted":
        if q.get("@type"):
            return Object.read(q)
        return SupergroupMembersFilter()
