"""
- This module is responsible for managing and providing uploader instances to upload files
"""

from .go_file_uploader import GoFileUploader
from .uploaders import BaseUploader


class UploaderManager:
    """
    UploadManager class to manage uploader
    """
    go_file_uploader = GoFileUploader
    anon_file_uploader = ""
    default = go_file_uploader
    uploader = {
        "go": go_file_uploader,
        "anon": anon_file_uploader,
    }

    @classmethod
    def get_uploader(cls, uploader: str) -> BaseUploader:
        """
        Returns the uploader depending on the string passed
        :param uploader: str
        :return: BaseUploader
        """
        loader = cls.uploader.get(uploader, cls.default)
        return loader()
