from aiogram import types

from tgbot.service.repository import SQLAlchemyRepos


async def any_handler(message: types.Message, repo: SQLAlchemyRepos):
    await message.answer(f'{message}', parse_mode='HTML')
