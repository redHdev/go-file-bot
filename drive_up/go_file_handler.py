"""
- This module is responsible to send the data related to gofile to driveup
"""

import requests

from config import config


class GoFileApiHandler:
    """
    Handler to send data about gofile to driveup
    """
    data_path = "data.downloadPage"
    def __init__(self, token: str, action: str):
        self.token = token
        self.action = action

    async def upload_data(self, json_data: dict) -> str:
        """
        Uploads the data to the api
        :param json_data:
        :return:
        """
        paths = self.data_path.split(".")
        tmp_data = json_data
        for path in paths:
            tmp_data = tmp_data.get(path)

        if tmp_data is None:
            status = "could not find the data needed to be sent to driveup"

        else:
            payload = {
                "data": tmp_data,
                "fid": self.token,
                "action": self.action,
            }
            res = requests.get(url=config.driveup_api_url, params=payload)
            status = f"drive up returned status: {res.status_code}"

        return status
