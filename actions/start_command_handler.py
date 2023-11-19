"""
- This module is responsible for handling the /start command, sent to the bot
"""

from pyrogram.types import Message

from config import config


INTRO = f"""
I am a file uploader bot, I can upload telegram files to servers.
I'm a closed source bot, so you must know how to work with the me.

I can't tell, how I work :)

__I'm processing files **{"SEQUENTIALLY" if config.sequentially else "PARALLELY"}**__
"""


async def handle_start_command(update: Message) -> None:
    """
    Handles the start command
    :param update: Message
    :return: None
    """
    tg_user = update.from_user
    await update.reply_text(
        text=f"Hello, {tg_user.mention}\n{INTRO}",
    )
