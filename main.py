"""
- Main entry point of the program
"""
import logging

logging.basicConfig(
    level=logging.INFO,
)

from bot import TelegramBot


if __name__ == "__main__":
    TelegramBot().run()
