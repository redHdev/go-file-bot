"""
- This module is responsible for handling the filemanager class
"""

from typing import Union

from pyrogram.types import Message

from .callback_manager import CallbackManager
from .telegram_file_processor import TelegramFileProcessor
from .url_file_processor import UrlFileProcessor


class FileManager:
    """
    FileManager class to return the proper fileprocessor to process downloads
    """
    telegram_file_processor = TelegramFileProcessor
    url_file_processor = UrlFileProcessor

    def __init__(self, file: Union[str, Message], callback_manager: CallbackManager):
        self.file = file
        self.cb_message = callback_manager

    def get_file_processor(self) -> Union[TelegramFileProcessor, UrlFileProcessor]:
        """
        Returns the file processor based on the file type
        :return:
        """
        if isinstance(self.file, Message):
            return self.telegram_file_processor(self.file, self.cb_message)

        else:
            return self.url_file_processor(self.file, self.cb_message)
