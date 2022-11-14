from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot import strings, bot, Config
from tgbot.keyboards import inline, reply
from tgbot.data import Button
from tgbot.states import forms
from tgbot.service.repository import SQLAlchemyRepos
from tgbot.service.user_repo import UserRepo
from tgbot.service.course_repo import CourseRepo
from tgbot.utils.courses import send_course_materials



async def subscribe2(call: types.CallbackQuery, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	user_id = call.from_user.id
	course_repo = repo.get_repo(CourseRepo)

	if call.data == 'check_subscription':
		status = await bot.get_chat_member(
			chat_id=Config.tgbot.channel_username, 
			user_id=user_id
		)
		if status.status != 'left':
			async with state.proxy() as data:
				course = await course_repo.get_course(name=data['course'])
				if course:
					existed = await course_repo.add_user_to_course(user_id=user_id, course_id=course.id)
					if existed is None:
						user_repo = repo.get_repo(UserRepo)
						user = await user_repo.get_user(user_id=user_id)
						if user:
							coins = user.mediana + 5
							await user_repo.update_user(user_id=user_id, data={"mediana": coins})
							await call.message.answer("🎉 Tabrilaymiz, siz ushbu kursga ro'yxatdan o'tganlingiz uchun *5* mediana coinga ega bo'ldingiz, ular orqali offline kurslarimizga chegirmalar olishingiz mumkin!")
				await send_course_materials(user_id=user_id, call=call, course_name=data['course'])
				await state.finish()
		else:
			await call.answer('Kanalga obuna b\'ling!')
			await forms.RegisterForm.subscibe.set()
	else:
		await call.answer('Kanalga obuna b\'ling!')
		await forms.RegisterForm.subscibe.set()
