from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot import strings, bot
from tgbot.keyboards import reply
from tgbot.service.repository import SQLAlchemyRepos



async def cancel_state(message: types.Message, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	await message.answer(
		text=strings.main_menu, 
		reply_markup=reply.menu()
	)
	await state.finish()
