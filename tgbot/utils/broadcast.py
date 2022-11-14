import csv
import asyncio

from aiogram.utils import exceptions
from datetime import datetime

from tgbot import strings, bot
from tgbot.config import get_file_path
from tgbot.keyboards import inline



async def broadcast_func(chat_id, copy_message_id, markup, user_repo):
	active_count = 0
	block_count = 0
	users_count = await user_repo.count_user()
	before = datetime.now()
	await bot.send_message(chat_id=chat_id, text=strings.yes)

	with open(f'{get_file_path()}/users.csv') as file_obj:
		reader_obj = csv.reader(file_obj)
		for user in reader_obj:
			try:
				await bot.copy_message(
					chat_id=user[0], 
					from_chat_id=chat_id, 
					message_id=copy_message_id, 
					reply_markup=inline.post_markup(markup)
				)
				active_count += 1
			except exceptions.RetryAfter as e:
				await asyncio.sleep(e.timeout)
				await bot.copy_message(
					chat_id=user[0], 
					from_chat_id=chat_id, 
					message_id=copy_message_id, 
					reply_markup=inline.post_markup(markup)
				)
				active_count += 1
			except:
				try:
					block_count += 1
					await user_repo.update_user(user_id=user[0], data={'blocked': True})
				except Exception as e:
					print(e)
			await asyncio.sleep(0.05)

	after = datetime.now()
	time_diff = after - before
	answer = f"*📊 Natija:*\n\n*👥 Jami obunachilar - *{users_count} ta"
	answer += f"\n*📤 Yuborildi - *{active_count} ta\n*🔐 Bloklaganlar - *{block_count} ta\n*🕔 Ketgan vaqt - *{time_diff}"
	await bot.send_message(chat_id=chat_id, text=answer)

