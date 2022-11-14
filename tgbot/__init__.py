from aiogram import Bot

from tgbot.config import load_config
from tgbot.data import Strings


Config = load_config()
bot = Bot(token=Config.tgbot.token, parse_mode='Markdown')
strings = Strings()
