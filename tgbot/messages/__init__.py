from aiogram import Dispatcher

from .message_handler import message_handler
from .any import any_handler


def register_messages(dp: Dispatcher) -> None:
    dp.register_message_handler(message_handler, state="*")
    dp.register_message_handler(any_handler, content_types=['photo', 'document'], state="*")
