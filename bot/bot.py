"""
- This module is responsible for handling the Telegram client
"""

import logging
import os
import sys

from pyrogram import Client
from pyrogram.errors import (
    ApiIdInvalid,
    ApiIdPublishedFlood,
    AuthKeyUnregistered,
    AuthKeyInvalid,
    AuthTokenExpired,
    AuthTokenInvalid,
    TokenInvalid,
)

from config import config


logger = logging.getLogger(__name__)


class TelegramBot(Client):
    """
    TelegramBot client to manage the bot
    """
    client: Client = None

    def __init__(self):
        super().__init__(
            name=self.__class__.__name__.lower(),
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=config.bot_token,
            plugins={"root": "handlers"},
            sleep_threshold=config.sleep_threshold,
            workdir=config.data_path,
            max_concurrent_transmissions=config.max_parallel_process,
        )

    def _remove_session_file(
        self,
        session_name: str = None,
    ) -> None:
        """
        Removes the session file
        :param session_name: str - name of the session
        """
        logger.info("trying to remove session file")
        if session_name is None:
            session_file_name = f"{self.__class__.__name__.lower()}.session"
        else:
            session_file_name = f"{session_name}.session"
        logger.info(f"session file name: {session_file_name}")
        if os.path.exists(session_file_name):
            logger.info(f"removing session file: {session_file_name}")
            try:
                os.remove(session_file_name)

            except Exception as e:
                error_text = "unexpected error occurred while removing session file. " \
                             f"Exception Type: {type(e)} | Value: {str(e)}"
                logger.exception(error_text)

            else:
                logger.info(f"removed session file: {session_file_name}")

    async def start(self) -> None:
        """
        Starts the bot and adds the plugins
        :return: None
        """
        print("starting bot...")
        logger.info("starting the bot")
        try:
            self.__class__.client = await super().start()

        except ApiIdInvalid:
            error_text = "api id/ api hash is invalid, kindly check and add the correct one."
            logger.exception(error_text)
            print(error_text)
            self._remove_session_file()
            sys.exit()

        except ApiIdPublishedFlood:
            error_text = "api id and api hash has been marked publicly available by telegram, kindly use" \
                         " different api id and api hash."
            logger.exception(error_text)
            print(error_text)
            self._remove_session_file()
            sys.exit()

        except AuthTokenExpired:
            error_text = "bot token used in the config file is expired. kindly update the bot token"
            logger.exception(error_text)
            print(error_text)
            self._remove_session_file()
            sys.exit()

        except (AuthKeyInvalid, AuthKeyUnregistered, AuthTokenInvalid, TokenInvalid):
            error_text = "authentication error occurred while starting the bot. kindly check the api id, api hash, " \
                         "and bot token, and try to restart the bot again."
            logger.exception(error_text)
            print(error_text)
            self._remove_session_file()
            sys.exit()

        except Exception as e:
            error_text = "unexpected error occurred while starting the bot. try restarting the bot once, " \
                         "if the issue persists, contact dev on telegram @haren0610 | " \
                         f"error type: {type(e)} | value: {str(e)}."
            logger.exception(error_text)
            print(error_text)
            self._remove_session_file()
            sys.exit()

        else:
            me = await self.get_me()
            info_text = f"bot started on @{me.username}"
            config.bot_link = f"https://t.me/{me.username}"
            logger.info(info_text)
            print(info_text)

    async def stop(self, *args) -> None:
        """
        Stops the bot and closes the program
        :return: None
        """
        logger.info("stopping the bot")
        print("stopping the bot...")
        try:
            await super().stop()

        except Exception as e:
            error_text = f"error occurred while stopping the bot. " \
                         f"exception type: {type(e)} | Value: {str(e)}"
            logger.error(error_text)

        finally:
            logger.info("bot stopped")

        print("Bot stopped. \nBye")
        sys.exit(0)
