from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.data import Button


def menu():
	markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

	markup.add(
		KeyboardButton(text=Button.free_courses), 

	)
	markup.add(
		KeyboardButton(text=Button.about_courses), 
		KeyboardButton(text=Button.locations)
	)
	markup.add(
		KeyboardButton(text=Button.coin), 

	)
	return markup

def back_to_menu():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)

	markup.add(
		KeyboardButton(text=Button.back_to_menu), 

	)
	return markup

def cancel_register():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)

	markup.add(
		KeyboardButton(text=Button.cancel_register), 

	)
	return markup

def request_contact():
	markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

	markup.add(
		KeyboardButton(text=Button.send_contact, request_contact=True), 
		KeyboardButton(text=Button.cancel_register), 

	)
	return markup
