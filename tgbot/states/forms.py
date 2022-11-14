from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterForm(StatesGroup):
	""" Student registration """

	course = State()
	full_name = State()
	phone = State()
	subscibe = State()


class SubscribeForm(StatesGroup):
	""" Subscribe """

	course = State()
	subscribe = State()


class BroadcastForm(StatesGroup):
	""" Broadcasting """

	chat_id = State()
	message_id = State()
	markup = State()
	yes_no = State()
