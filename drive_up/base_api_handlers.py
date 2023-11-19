"""
- This module is responsible for providing interface to upload data on drive up
"""

from abc import ABCMeta, abstractmethod


class BaseApiHandler(metaclass=ABCMeta):
    """
    BaseApiHandler to manage the api requests
    """

    @abstractmethod
    async def upload_data(self, json_data: dict) -> None:
        """
        Upload the data to the api
        :param json_data:
        :return:
        """
        raise NotImplemented("haven't been implemented")
