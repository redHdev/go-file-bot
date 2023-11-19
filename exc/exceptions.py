"""
- This module is responsible to manage the exceptions thrown at runtime
"""

class Error(Exception):
    """
    Base exception for the program
    """
    default_msg = "unknown error occurred"

    def __init__(self, msg: str = None):
        self.msg = msg or self.default_msg


class BestGoServerNotFound(Error):
    """
    Thrown when we can not find the best go server
    """
    default_msg = "couldn't find the best go server to upload files"

    def __init__(self, msg: str = None):
        self.msg = msg or self.default_msg
