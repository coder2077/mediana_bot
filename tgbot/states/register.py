from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot import strings, bot, Config
from tgbot.keyboards import inline, reply
from tgbot.data import Button
from tgbot.states import forms
from tgbot.service.repository import SQLAlchemyRepos
from tgbot.service.user_repo import UserRepo
from tgbot.service.course_repo import CourseRepo
from tgbot.utils.validators import validate_phone
from tgbot.utils.courses import send_course_materials



async def get_full_name(message: types.Message, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	text = message.text

	if message.content_type == 'text':
		if len(text.split()) == 2 or len(text.split()) == 3:
			await state.update_data({'full_name': text})
			await message.answer(text=strings.get_phone, reply_markup=reply.request_contact())
			await forms.RegisterForm.phone.set()
		else:
			await message.answer(text=strings.not_full_name)
			await forms.RegisterForm.full_name.set()
	else:
		await message.answer(text=strings.not_full_name)
		await forms.RegisterForm.full_name.set()


async def get_phone(message: types.Message, repo: SQLAlchemyRepos, state: FSMContext) -> None:
	user_id = message.from_user.id
	text = message.text

	user_repo = repo.get_repo(UserRepo)
	user = await user_repo.get_user(user_id=user_id)

	if message.content_type == 'text':
		validation = validate_phone(text=text)
		if validation == True:
			await state.update_data({'phone': text})
			async with state.proxy() as data:
				if user:
					pay_data = {
						'full_name': data['full_name'], 
						'phone': text, 
						'registered': True
					}
					await user_repo.update_user(user_id=user_id, data=pay_data)
					await message.answer(text=strings.subscribe, reply_markup=inline.subscribe_to_channel(), parse_mode='html')
					await forms.RegisterForm.subscibe.set()
				else:
					await user_repo.add_user(
						user_id=user_id, 
						full_name=data['full_name'], 
						phone=text, 
						registered=True, 
						referral=None
					)
					await message.answer(text=strings.subscribe, reply_markup=inline.subscribe_to_channel(), parse_mode='html')
					await forms.RegisterForm.subscibe.set()
		else:
			await message.answer(text=strings.not_phone)
			await forms.RegisterForm.phone.set()

	elif message.content_type == 'contact':
		contact = message.contact.phone_number
		await state.update_data({'phone': contact})
		async with state.proxy() as data:
			if user:
				pay_data = {
					'full_name': data['full_name'], 
					'phone': contact, 
					'registered': True
				}
				await user_repo.update_user(user_id=user_id, data=pay_data)
				await message.answer(text=strings.subscribe, reply_markup=inline.subscribe_to_channel(), parse_mode='html')
				await forms.RegisterForm.subscibe.set()
			else:
				await user_repo.add_user(
					user_id=user_id, 
					full_name=data['full_name'], 
					phone=contact, 
					registered=True, 
					referral=None
				)
				await message.answer(text=strings.subscribe, reply_markup=inline.subscribe_to_channel(), parse_mode='html')
				await forms.RegisterForm.subscibe.set()

	else:
		await message.answer(text=strings.not_phone)
		await forms.RegisterForm.phone.set()


async def subscribe(call: types.CallbackQuery, repo: SQLAlchemyRepos, state: FSMContext) -> None:
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
							await user_repo.update_user(user_id=user_id, data={"mediana": 10})
							await call.message.answer("🎉 Tabrilaymiz, siz botdan ro'yxatdan o'tganlingiz uchun *5* mediana coinga ega bo'ldingiz, ular orqali offline kurslarimizga chegirmalar olishingiz mumkin!")

				await send_course_materials(user_id=user_id, call=call, course_name=data['course'])
				await state.finish()
		else:
			await call.answer('Kanalga obuna b\'ling!')
			await forms.RegisterForm.subscibe.set()
	else:
		await call.answer('Kanalga obuna b\'ling!')
		await forms.RegisterForm.subscibe.set()
