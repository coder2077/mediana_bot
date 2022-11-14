from aiogram import Dispatcher

from .callback_query_handler import callback_handler


def register_callbacks(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(callback_handler, state="*")
