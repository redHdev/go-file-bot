"""
- This module is responsible for handling the upload command
"""
import asyncio
import logging
from typing import List, Optional, Union
from urllib.parse import urlparse

from pyrogram.types import Message

from config import config
from drive_up import GoFileApiHandler
from uploaders import CallbackManager, UploaderManager

log = logging.getLogger(__name__)
command_not_formatted = "command not formatted properly"
_expected_length = 4


class UploadHandler:
    """
    Upload handler class to manage the uploads
    """
    processing: List["UploadHandler"] = []
    queue: List["UploadHandler"] = []

    def __init__(self, update: Message):
        log.info("instantiating upload handler for update: %d", update.id)
        self.update = update
        self.cb_message: Optional[Message] = None
        self.file: Union[str, Message, None] = None
        self.token: Optional[str] = None

    def get_file(self) -> Union[str, Message, None]:
        """
        Returns the file if it's available else returns None
        :return:
        """
        log.info("getting file for handler: %d", self.update.id)
        file = None
        update = self.update
        if update.text:
            if len(update.command) != _expected_length:
                log.warning("received a text command of len: %d", len(update.command))

            else:
                url = update.command[1]
                try:
                    result = urlparse(url)

                except ValueError:
                    log.warning("value error occurred while verifying the url: %s", url)

                else:
                    if all(
                            [result.scheme, result.netloc, ],
                    ):
                        log.info("valid url received: %s", url)
                        file = url

        # if processing files
        else:
            log.info("processing telegram file")
            if len(update.command) == _expected_length - 1:
                file = update

        self.file = file
        return file

    def get_token(self) -> str:
        """
        Returns the token
        :return:
        """
        token = self.update.command[-2]
        log.info("returning token: %s", token)
        return token

    def get_action(self) -> str:
        """
        Returns the action
        :return:
        """
        action = self.update.command[-1]
        log.info("returning action: %s", action)
        return action

    async def send_command_not_formatted_properly(self) -> None:
        """
        Sends, command not formatted properly
        :return:
        """
        log.info("sending command not formatted properly for update: %d", self.update.id)
        await self.update.reply_text(
            text=command_not_formatted,
            quote=True,
        )

    async def send_in_queue(self) -> None:
        """
        Sends that the file is in queue
        :return:
        """
        log.info("sending handler in queue for update: %d", self.update.id)
        self.cb_message = await self.update.reply_text(
            text="In queue",
            quote=True,
        )

    async def process_upload(self) -> None:
        """
        process upload
        :return:
        """
        log.info("processing handler with update: %d", self.update.id)
        cls = self.__class__
        process = True
        # if already processing a file
        if len(cls.processing) > 0:
            log.info("processing more than one handler")
            # if we are processing the files one by one
            if config.sequentially:
                # append in the queue
                log.info("appending the handler in queue because currently processing files sequentially")
                cls.queue.append(self)
                process = False

            else:
                if len(cls.processing) >= config.max_parallel_process:
                    log.info("appending the handler in queue because currently processing files more than threshold")
                    cls.queue.append(self)
                    process = False

        # if we are not processing now
        if not process:
            await self.send_in_queue()

        # if we are processing
        else:
            cls.processing.append(self)
            log.info(
                "added handler with update %d to the processing queue, current queue: %s",
                self.update.id, cls.processing
            )
            loader = "go"
            log.info("getting uploader for %s", loader)
            uploader = UploaderManager.get_uploader(loader)
            processing_text = "processing..."
            if self.cb_message:
                log.info("editing existing cb message for handler with update: %d", self.update.id)
                await self.update.edit_text(
                    text=processing_text,
                )

            else:
                log.info("sending cb message for handler with update: %d", self.update.id)
                self.cb_message = await self.update.reply_text(
                    text=processing_text,
                    quote=True,
                )

            cb_manager = CallbackManager(self.cb_message)
            log.info("uploading file for handler with update: %d", self.update.id)
            token = self.get_token()
            action = self.get_action()
            api_handler = GoFileApiHandler(
                token=token,
                action=action,
            )
            upload = uploader.upload(
                file=self.file,
                cb_manager=cb_manager,
                api_handler=api_handler,
            )
            # may it help
            loop = asyncio.get_event_loop()
            task = loop.create_task(upload)
            await task
            log.info("removing handler from queue")
            cls.processing.remove(self)
            log.info("removed handler from processing queue, current queue: %s", cls.processing)
            if cls.queue:
                # removing the handler from queue
                handler = cls.queue.pop(0)
                log.info("popped handler with id: %d from queue, current queue: %s", handler.update.id, cls.queue)
                # trying to process it
                await handler.process_upload()


async def handle_upload_command(update: Message) -> None:
    """
    Handles the upload command
    :param update:
    :return:
    """
    handler = UploadHandler(update=update)
    file = handler.get_file()
    if file is None:
        await handler.send_command_not_formatted_properly()

    else:
        await handler.process_upload()
