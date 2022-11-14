import phonenumbers


def validate_phone(text: str):
	if text.startswith('+998'):
		phone_string = text
	else:
		phone_string = f"+998{text}"
	try:
		my_number = phonenumbers.parse(phone_string)
		return phonenumbers.is_valid_number(my_number)
	except:
		return False
