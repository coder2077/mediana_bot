from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.data import Button


def courses_menu():
	markup = InlineKeyboardMarkup(row_width=1)

	markup.add(
		InlineKeyboardButton(text=Button.course_1, callback_data=Button.course_1), 
		InlineKeyboardButton(text=Button.course_2, callback_data=Button.course_2), 
		InlineKeyboardButton(text=Button.course_3, callback_data=Button.course_3), 
		InlineKeyboardButton(text=Button.course_4, callback_data=Button.course_4), 
		InlineKeyboardButton(text=Button.course_5, callback_data=Button.course_5), 
		InlineKeyboardButton(text=Button.back_to_menu, callback_data='back_to_menu'), 
	)
	return markup

def subscribe_to_channel():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text=Button.channel, url=Button.channel_url), 
        InlineKeyboardButton(text=Button.check_subscription, callback_data='check_subscription'), 
    )
    return markup

def post_markup(data):
	markup = InlineKeyboardMarkup()
	if data:
		buttons = data.split("\n")
		for button in buttons:
			button = button.split(" + ")
			btn = InlineKeyboardButton(text=button[0], url=button[1])
			markup.add(btn)
		return markup
	return None

def confirm_broadcast(data=None):
	try:
		markup = InlineKeyboardMarkup()
		if data:
			buttons = data.split("\n")
			for button in buttons:
				button = button.split(" + ")
				btn = InlineKeyboardButton(text=button[0], url=button[1])
				markup.add(btn)

		btn1 = InlineKeyboardButton("✔️ Yuborish", callback_data="yes")
		btn2 = InlineKeyboardButton("✖️ Bekor qilish", callback_data="no")
		markup.add(btn1, btn2)
		return markup
	except:
		btn1 = InlineKeyboardButton("✔️ Yuborish", callback_data="yes")
		btn2 = InlineKeyboardButton("✖️ Bekor qilish", callback_data="no")
		markup.add(btn1, btn2)
		return markup
