"""
- This module is responsible for handling the messages sent to the bot
"""
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from actions import (
    handle_start_command,
    handle_upload_command,
)
from bot import TelegramBot
from config import config


log = logging.getLogger(__name__)


@TelegramBot.on_message(filters.command("id"))
async def id_command_handler(_: Client, update: Message) -> None:
    """
    Handles the /id command
    :param _: Client
    :param update: Message
    :return: None
    """
    log.info("id command received from chat: %d", update.chat.id)
    await update.reply_text(
        text=f"ChatID: `{update.chat.id}`",
    )

@TelegramBot.on_message(filters.private & filters.command("start"))
async def start_command_handler(_: Client, update: Message) -> None:
    """
    Handles the /start command
    :param _: Client
    :param update: Message
    :return: None
    """
    log.info("start command received from user: %d, chat: %d", update.from_user.id, update.chat.id)
    await handle_start_command(update)


@TelegramBot.on_message(filters.chat(config.main_channel_id) & filters.command("upload"))
async def upload_command_handler(_: Client, update: Message) -> None:
    """
    Handles the /upload command
    :param _: Client
    :param update: Message
    :return: None
    """
    log.info("upload command received from chat: %d", update.chat.id)
    await handle_upload_command(update)
