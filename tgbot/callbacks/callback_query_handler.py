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



async def callback_handler(call: types.CallbackQuery, repo: SQLAlchemyRepos, state: FSMContext):
	user_id = call.from_user.id
	name = call.message.from_user.first_name
	full_name = call.from_user.full_name
	username = call.from_user.username

	user_repo = repo.get_repo(UserRepo)
	course_repo = repo.get_repo(CourseRepo)
	user = await user_repo.get_user(user_id=user_id)

	if user:
		text = call.data

		if text in [Button.course_1]:
			if user.registered == True:
				status = await bot.get_chat_member(
					chat_id=Config.tgbot.channel_username, 
					user_id=user_id
				)
				if status.status != 'left':
					course = await course_repo.get_course(name=text)
					if course:
						existed = await course_repo.add_user_to_course(user_id=user.user_id, course_id=course.id)
						if existed is None:
							coins = user.mediana + 5
							await user_repo.update_user(user_id=user_id, data={"mediana": coins})
							await call.message.answer("🎉 Tabrilaymiz, siz ushbu kursga ro'yxatdan o'tganlingiz uchun *5* mediana coinga ega bo'ldingiz, ular orqali offline kurslarimizga chegirmalar olishingiz mumkin!")
					await send_course_materials(user_id=user_id, call=call, course_name=text)
				else:
					await call.message.answer(text=strings.subscribe, reply_markup=inline.subscribe_to_channel(), parse_mode='html')
					await forms.SubscribeForm.subscribe.set()
					await state.update_data({'course': text})
					await call.message.delete()
			else:
				await call.message.answer(
					text=strings.get_full_name, 
					reply_markup=reply.cancel_register()
				)
				await forms.RegisterForm.full_name.set()
				await state.update_data({'course': text})
				await call.message.delete()

		elif text == 'back_to_menu':
			await call.message.delete()
			await call.message.answer(
				text=strings.main_menu, 
				reply_markup=reply.menu()
			)
		
		elif text in [Button.course_2, Button.course_3, Button.course_4, Button.course_5]:
			await call.message.answer(
				text="Tez orada bu kurslar to'ldiriladi..."
			)

	else:
		await user_repo.add_user(
			user_id=user_id,
			full_name=full_name,
			username=username,
			referral=None
		)
		await call.message.answer(text=strings.start_message.format(name=name), reply_markup=reply.menu(), parse_mode=None)
