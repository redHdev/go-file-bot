"""
- This module implements GoFileUploader class
This class is responsible to handle file uploading to the go file servers
"""
import asyncio
import json
import logging
from typing import Union

from aiohttp import ClientSession, ClientTimeout, FormData
from pyrogram.types import Message

from .callback_manager import CallbackManager
from .uploaders import BaseUploader
from .file_manager import FileManager
from .url_file_processor import UrlFileProcessor
from config import config
from drive_up import GoFileApiHandler
from exc import BestGoServerNotFound


log = logging.getLogger(__name__)


class GoFileUploader(BaseUploader):
    """
    GoFileUploader class to manage uploading files to gofile.io
    """
    best_server_key = "best_server"
    api_base_url = "https://api.gofile.io"
    _get_server_path = "/getServer"
    get_best_server_url = api_base_url + _get_server_path
    best_server_json_path = "data.server"
    upload_api_url = f"https://{best_server_key}.gofile.io/uploadFile"

    def __init__(self):
        log.info("initializing a go file uploader object")

    async def set_uploader_url(self, session: ClientSession) -> None:
        """
        Sets the uploader url for uploading files
        :param session: ClientSession
        :return: None
        """
        log.info("trying to get the best upload api url")
        async with session.get(url=self.get_best_server_url) as res:
            try:
                log.info("trying to decode the response as json")
                json_data = await res.json()

            except json.JSONDecoder:
                error_message = "json decode error occurred while requesting gofile.io for best server to upload file"
                log.exception(error_message)
                raise BestGoServerNotFound(
                    msg=error_message,
                )

            else:
                paths = self.best_server_json_path.split(".")
                data = None
                for path in paths:
                    try:
                        data = json_data[path]
                        json_data = data

                    except KeyError:
                        error_message = f"key {path} not found in the json received from gofile.io"
                        log.exception(error_message)
                        raise BestGoServerNotFound(
                            msg=error_message,
                        )

                    except TypeError:
                        error_message = f"data of unknown type set as json: {json_data}, key: {path}"
                        log.exception(error_message)
                        raise BestGoServerNotFound(
                            msg=error_message,
                        )

                else:
                    if data is None:
                        error_message = "unknown error occurred while getting the best gofile.io server"
                        log.error(error_message)
                        raise BestGoServerNotFound(
                            msg=error_message,
                        )

                    self.upload_api_url = self.upload_api_url.replace(self.best_server_key, data)
                    log.info("best upload api url found: %s", self.upload_api_url)

    async def upload(
        self,
        file: Union[str, Message],
        cb_manager: CallbackManager,
        api_handler: GoFileApiHandler,
    ) -> None:
        """
        Uploads the file to the server if everything is good
        :param file: Path
        :param cb_manager: Message
        :param api_handler: GoFileApiHandler
        :return: None
        """
        log.info("trying to upload files")
        timeout = ClientTimeout(config.upload_timeout)
        file_processor = FileManager(
            file=file,
            callback_manager=cb_manager,
        ).get_file_processor()
        file_name = await file_processor.get_file_name()
        async with ClientSession(timeout=timeout) as session:
            # setting session for url file processor to work
            if isinstance(file_processor, UrlFileProcessor):
                await file_processor.set_session(session=session)

            await self.set_uploader_url(session=session)
            data = FormData()
            data.add_field(
                "file", file_processor.get_data(), content_type="application/octet-stream",
                filename=file_name,
            )
            async with session.post(
                url=self.upload_api_url,
                data=data,
            ) as response:
                json_data = await response.json()
                # updating the data on message
                await cb_manager.completed(json_data=json_data)
                # sending data to drive up
                final_data = await api_handler.upload_data(json_data=json_data)
                await asyncio.sleep(1)
                # sending response from driveup to telegram
                await cb_manager.send_final_data(
                    data=final_data,
                )
