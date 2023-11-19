"""
- This module is responsible for processing the files
"""

from abc import ABCMeta, abstractmethod
from typing import AsyncIterable

from pyrogram.types import Message


class BaseFileProcessor(metaclass=ABCMeta):
    """
    BaseFileProcessor class to define rules of file processing
    """

    @abstractmethod
    async def get_file_name(self) -> str:
        """
        Returns the file name of the file
        :return: str
        """
        raise NotImplemented("haven't implemented yet")

    @abstractmethod
    async def get_data(self) -> AsyncIterable:
        """
        Returns the data of the file
        :return:
        """
        raise NotImplemented("haven't implemented yet")
