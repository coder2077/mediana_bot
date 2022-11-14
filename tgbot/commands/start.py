from aiogram import types
from redis import Redis

from tgbot import strings
from tgbot.keyboards import reply
from tgbot.service.repository import SQLAlchemyRepos
from tgbot.service.user_repo import UserRepo
from tgbot.states import forms



r = Redis(
	host='redis-16500.c73.us-east-1-2.ec2.cloud.redislabs.com', 
	port=16500, 
	password='wz61H13hTzFDT6bBtAVY6AGowyOcUorS'
)

async def cmd_start(message: types.Message, repo: SQLAlchemyRepos):
	user_id = message.from_user.id
	name = message.from_user.first_name
	full_name = message.from_user.full_name
	username = message.from_user.username
	args = message.get_args()

	user_repo = repo.get_repo(UserRepo)
	user = await user_repo.get_user(user_id=user_id)

	if args.startswith('broadcast_'):
		data = args.replace('broadcast_', '')
		password = r.get('password')
		if password:
			if data == password.decode('ascii'):
				r.delete('password')
				await message.answer(text=strings.get_content)
				await forms.BroadcastForm.chat_id.set()			
			else:
				await message.answer(strings.not_admin)
		else:
			await message.answer(strings.not_admin)
	else:
		if user is None:
			if args in ['instagram', 'facebook', 'telegram']:
				ref = args
			
			else:
				ref = None
			await user_repo.add_user(
				user_id=user_id,
				full_name=full_name,
				username=username,
				referral=ref
			)
			await message.answer(text=strings.start_message.format(name=name), reply_markup=reply.menu(), parse_mode=None)

		else:
			await message.answer(text=strings.start_message.format(name=name), reply_markup=reply.menu(), parse_mode=None)
