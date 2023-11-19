"""
- This module is responsible for handling the telegram files
"""

from typing import AsyncIterable

from pyrogram.types import Message

from .callback_manager import CallbackManager
from .file_processors import BaseFileProcessor
from bot import TelegramBot


class TelegramFileProcessor(BaseFileProcessor):
    """
    TelegramFileProcessor class to process telegram files
    """

    def __init__(self, msg: Message, callback_manager: CallbackManager):
        self.message = msg
        self.callback_manager = callback_manager
        self.file = msg.document or msg.audio or msg.video or msg.photo or msg.animation or msg.media

    async def get_file_name(self) -> str:
        """
        Returns the file name of the file
        :return: str
        """
        return self.file.file_name

    async def get_data(self) -> AsyncIterable:
        """
        Returns the file data
        :return:
        """
        client = TelegramBot.client
        await self.callback_manager.start(
            total_size=self.file.file_size,
        )
        async for chunk in client.stream_media(message=self.message):
            await self.callback_manager.downloaded(
                downloaded=len(chunk),
            )
            yield chunk
