from aiogram import types

from tgbot import strings, bot
from tgbot.keyboards import inline, reply
from tgbot.data import Button
from tgbot.service.repository import SQLAlchemyRepos
from tgbot.service.user_repo import UserRepo



async def message_handler(message: types.Message, repo: SQLAlchemyRepos):
	user_id = message.from_user.id
	name = message.from_user.first_name
	full_name = message.from_user.full_name
	username = message.from_user.username

	user_repo = repo.get_repo(UserRepo)
	user = await user_repo.get_user(user_id=user_id)

	if user:
		text = message.text

		if text == Button.about_courses:
			await message.answer(
				text=strings.about_courses, 
				reply_markup=reply.back_to_menu()
			)

		elif text == Button.locations:
			await message.answer_location(
				latitude=41.38806341672505, longitude=69.45944062698521, reply_markup=reply.menu()
			)

		elif text == Button.free_courses:
			await message.answer(
				text=strings.free_courses, 
				reply_markup=inline.courses_menu()
			)
		
		elif text == Button.coin:
			await message.answer(
				text=strings.your_coin.format(coin=user.mediana), 
				reply_markup=reply.menu()
			)

		elif text == Button.back_to_menu:
			await message.answer(
				text=strings.main_menu, 
				reply_markup=reply.menu()
			)

	else:
		await user_repo.add_user(
			user_id=user_id,
			full_name=full_name,
			username=username,
			referral=None
		)
		await message.answer(text=strings.start_message.format(name=name), reply_markup=reply.menu(), parse_mode=None)
