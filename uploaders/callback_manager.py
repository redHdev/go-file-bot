"""
- This module is responsible for managing callback process
"""
import json
import time
from datetime import datetime, timedelta
from typing import Optional

from pyrogram.types import Message

from .uploaders import BaseUploader


class CallbackManager:
    """
    CallbackManager class to manage the callbacks
    """
    progress_threshold = 10     # send update if progress is more than 10%
    time_threshold = timedelta(seconds=5)   # send update if not sent any for this time

    def __init__(self, msg: Message):
        self.msg = msg
        self.start_time: Optional[float] = None
        self.last_sent: Optional[datetime] = None
        self.total_size: float = 0
        self.bytes_read: float = 0
        self.last_progress: float = 0
        self.recent_progress: float = 0

    async def start(self, total_size: float) -> None:
        """
        Starts the download
        :return:
        """
        self.total_size = total_size
        self.start_time = time.monotonic()
        await self.msg.edit_text(
            text="Starting upload...",
        )

    def calculate_details(self) -> str:
        """
        Returns the data aboutn progress
        :return: str
        """
        time_taken = time.monotonic() - self.start_time
        speed = self.bytes_read / time_taken
        cal_speed = speed

        # if the speed is more than 1 MB/s
        if speed > BaseUploader.MEGA_BYTE:
            cal_speed /= BaseUploader.MEGA_BYTE
            unit = "MB/s"

        else:
            cal_speed /= BaseUploader.MEGA_BYTE
            unit = "KB/s"

        progress = self.bytes_read / self.total_size * 100
        self.recent_progress = progress
        remaining_size = self.total_size - self.bytes_read
        remaining_time = remaining_size / speed if speed > 0 else 0
        status_message = f"Progress: {progress:.2f}%\n" \
                         f"Speed: {cal_speed:.2f} {unit}\n" \
                         f"Total Time: {timedelta(seconds=round(time_taken))}\n" \
                         f"ETA: {timedelta(seconds=round(remaining_time))}"

        return status_message

    async def update_status(self) -> None:
        """
        Updates the status of the message
        :return:
        """
        self.last_sent = datetime.utcnow()
        self.last_progress = self.recent_progress
        await self.msg.edit_text(
            text=self.calculate_details(),
        )

    async def downloaded(self, downloaded: float) -> None:
        """
        Updates that some part has been downloaded
        :param downloaded: float
        :return:
        """
        self.bytes_read += downloaded
        self.calculate_details()
        if self.need_to_send():
            await self.update_status()

    def need_to_send(self) -> bool:
        """
        Checks whether to send the update or not
        :return:
        """
        status = False
        if self.last_sent is None:
            status = True

        else:
            progressed = self.last_progress - self.recent_progress
            if progressed >= self.progress_threshold:
                status = True

            else:
                now = datetime.utcnow()
                spent = now - self.last_sent
                if spent >= self.time_threshold:
                    status = True

        return status

    async def completed(self, json_data: dict) -> None:
        """
        Updates the completed status
        :param json_data:
        :return:
        """
        data = json.dumps(json_data, indent=4)
        await self.msg.edit_text(
            text="UPLOADED SUCCESSFULLY\n"
                 "```json\n"
                 f"{data}\n"
                 f"```",
        )

    async def send_final_data(self, data: str) -> None:
        """
        Sends final data
        :param data:
        :return:
        """
        await self.msg.edit_text(
            text=data,
        )
