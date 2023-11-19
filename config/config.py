"""
- This module is responsible for handling the configurations of the program
"""
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)


@dataclass
class Config:
    """
    Config class to store configuration details
    """
    # CHANGE THESE ACCORDING TO NEED -----------------------------------------------------------------------------------
    # enter your telegram api id here
    api_id: int = 
    # enter your telegram api hash here
    api_hash: str = ""
    # enter your telegram bot token here
    bot_token: str = ""
    # want to process links and files one by one?
    # if yes, make it True
    # if you want to process multiple files parallely then make it False
    sequentially: bool = False
    # how many files should be processed parallely, applicable only if sequential is False
    max_parallel_process: int = 4
    # how to get the channel ids?
    # add the bot to the channels as admin and send /id in the channels, bot will reply the id of the channel
    # enter the channel id of the channel where all the logs are going to be sent
    log_channel_id: int = -100
    # enter the channel id of the channel, from where bot will process the links and files
    main_channel_id: int = -1001952870573
    # api url of drive up
    driveup_api_url: str = "https://driveup.sbs/red.php"
    # upload timeout, in seconds, make it None, if you want no timeout
    upload_timeout: Optional[int] = None

    # __________________________________________________________________________________________________________________

    # NO NEED TO CHANGE THESE ------------------------------------------------------------------------------------------
    one_minute: int = 60
    sleep_threshold: int = 3 * one_minute
    project_name: str = "go-file-bot"
    data_path: Path = Path(project_name)
    log_level = logging.WARNING
    bot_link: str = None

    # __________________________________________________________________________________________________________________

    def __post_init__(self):
        self.data_path.mkdir(exist_ok=True)


class TestConfig(Config):
    """
    TestConfig class to manage configurations of tests
    """
    log_level = logging.INFO


if os.environ.get("TEST", False):
    config = TestConfig()

else:
    config = Config()

logging.info("using config: %s", config)
