"""
- This module is responsible for UrlFilProcessor Class
"""
import os.path
from urllib.parse import urlparse
from typing import AsyncIterable, Optional

from aiohttp import ClientSession

from .callback_manager import CallbackManager
from .file_processors import BaseFileProcessor


class UrlFileProcessor(BaseFileProcessor):
    """
    UrlFileProcessor to process files from url
    """

    def __init__(self, file: str, callback_manager: CallbackManager):
        self.file = file
        self.callback_manager = callback_manager
        self.session: Optional[ClientSession] = None

    async def get_file_name(self) -> str:
        """
        :return:
        """
        result = urlparse(self.file)
        path = result.path
        file_name = os.path.basename(path)
        return file_name

    async def get_file_size(self) -> float:
        """
        Returns the file size
        :return: float
        """
        async with self.session.head(self.file) as r:
            headers = r.headers
            length = headers.get("content-length")
            if length is None:
                length = 0

            return float(length)

    async def set_session(self, session: ClientSession) -> None:
        """
        Sets the session
        :param session:
        :return:
        """
        self.session = session

    async def get_data(self) -> AsyncIterable:
        """
        Returns the data of the file
        :return:
        """
        file_size = await self.get_file_size()
        await self.callback_manager.start(
            total_size=file_size,
        )
        async with self.session.get(url=self.file) as r:
            while True:
                chunk = await r.content.read(16144)
                if not chunk:
                    break

                else:
                    await self.callback_manager.downloaded(downloaded=len(chunk))
                    yield chunk
