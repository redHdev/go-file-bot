"""
- This module is responsible for handling upload related tasks
"""

from abc import ABCMeta, abstractmethod
from typing import Union

from pyrogram.types import Message

from . import callback_manager
from drive_up import GoFileApiHandler


class BaseUploader(metaclass=ABCMeta):
    """
    BaseUploader Meta class to define behaviour of uploader classes
    """
    BYTE: int = 1
    KILO_BYTE: int = 1024 * BYTE
    MEGA_BYTE: int = 1024 * KILO_BYTE
    CHUNK_SIZE: int = MEGA_BYTE

    @abstractmethod
    async def upload(
        self,
        file: Union[str, Message],
        cb_manager: "callback_manager.CallbackManager",
        api_handler: GoFileApiHandler,
    ) -> None:
        """
        Uploads the file
        :param file:
        :param cb_manager:
        :return:
        """
        raise NotImplemented("haven't been implemented yet")
