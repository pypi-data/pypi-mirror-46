

from ..utils import Object


class FileType(Object):
    """
    Represents the type of a file

    No parameters required.
    """
    ID = "fileType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "FileTypeSecretThumbnail or FileTypeVideo or FileTypeVoiceNote or FileTypeVideoNote or FileTypeUnknown or FileTypeSticker or FileTypePhoto or FileTypeAnimation or FileTypeProfilePhoto or FileTypeDocument or FileTypeSecure or FileTypeSecret or FileTypeNone or FileTypeThumbnail or FileTypeAudio or FileTypeWallpaper":
        if q.get("@type"):
            return Object.read(q)
        return FileType()
