from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot import strings, bot
from tgbot.keyboards import inline, reply
from tgbot.data import Button
from tgbot.states import forms
from tgbot.service.repository import SQLAlchemyRepos
from tgbot.service.user_repo import UserRepo
from tgbot.utils.broadcast import broadcast_func



async def get_content(message: types.Message, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	chat_id = message.chat.id
	message_id = message.message_id

	await state.update_data({'chat_id': chat_id, 'message_id': message_id})
	await message.answer(text=strings.get_markup)
	await forms.BroadcastForm.markup.set()


async def get_markup(message: types.Message, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	user_id = message.from_user.id
	text = message.text

	async with state.proxy() as data:
		chat_id = data['chat_id']
		message_id_broadcast = data['message_id']
	
		if text == '/nobutton':
			await state.update_data({'markup': None})
			await bot.copy_message(
				chat_id=user_id, 
				from_chat_id=chat_id, 
				message_id=message_id_broadcast, 
				reply_markup=inline.confirm_broadcast(data=text)
			)
			await forms.BroadcastForm.yes_no.set()

		else:
			await bot.copy_message(
				chat_id=user_id, 
				from_chat_id=chat_id, 
				message_id=message_id_broadcast, 
				reply_markup=inline.confirm_broadcast(data=text)
			)
			await state.update_data({'markup': text})
			await forms.BroadcastForm.yes_no.set()


async def yes_no(call: types.CallbackQuery, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	user_repo = repo.get_repo(UserRepo)

	if call.data == 'yes':
		async with state.proxy() as data:
			chat_id = data['chat_id']
			copy_message_id = data['message_id']
			markup = data['markup']

			await broadcast_func(
				chat_id=chat_id, 
				copy_message_id=copy_message_id, 
				markup=markup, 
				user_repo=user_repo
			)
		await state.finish()

	else:
		await call.message.edit_text(
			text=strings.no
		)
		await state.finish()
