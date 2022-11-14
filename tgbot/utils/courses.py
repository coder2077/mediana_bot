from aiogram import types

from tgbot import strings, bot, Config
from tgbot.keyboards import reply
from tgbot.data import Button



async def send_course_materials(user_id: int, call: types.CallbackQuery, course_name: int):
	if course_name == Button.course_1:
		try:
			await call.message.delete()
		except:
			pass
		await call.message.answer(
			text=strings.course_1_text, 
			reply_markup=reply.back_to_menu()
		)
		await call.message.answer_document(
			document='BQACAgIAAxkBAAIHjWNSrXkKSwgHzG1Z-yiQ0H-XOU5oAAKzIwACjUZZSPo1OhKaWt2PKgQ', 
			thumb='AAMCAgADGQEAAgeNY1KteQpLCAfMbVn7KJDQf5c5TmgAArMjAAKNRllI-jU6Eppa3Y8BAAdtAAMqBA', 
			caption='1-dars'
		)
		await call.message.answer_document(
			document='BQACAgIAAxkBAAIHj2NSre8C_aKL3orzwBy4mZxOi4r1AALZIAACIE7RSGwb0ITHlYn-KgQ', 
			thumb='AAMCAgADGQEAAgePY1Kt7wL9ooveivPAHLiZnE6LivUAAtkgAAIgTtFIbBvQhMeVif4BAAdtAAMqBA', 
			caption='2-dars'
		)


	elif course_name == Button.course_2:
		try:
			await call.message.delete()
		except:
			pass
		await call.message.answer_document(
			document='BQACAgIAAxkBAAIJZWNyjTHJduk5tUezK5DajAot1ul0AAKmIQACa-l5S_vq4g7bcFtaKwQ', 
			caption="Robototexnika kursi elektron darsligi.", 
			reply_markup=reply.back_to_menu()
		)
