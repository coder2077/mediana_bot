from aiogram.types import ContentTypes
from aiogram import Dispatcher

from tgbot.states.forms import RegisterForm, SubscribeForm, BroadcastForm
from tgbot.data import Button

from .cancel import cancel_state
from .register import get_full_name, get_phone
from .register import subscribe
from .subscribe_ch import subscribe2
from .broadcast import get_content, get_markup, yes_no



def register_states(dp: Dispatcher) -> None:
	dp.register_message_handler(cancel_state, lambda message: message.text == Button.cancel_register, state='*')
	dp.register_message_handler(get_full_name, content_types=ContentTypes.ANY, state=RegisterForm.full_name)
	dp.register_message_handler(get_phone, content_types=ContentTypes.ANY, state=RegisterForm.phone)

	dp.register_callback_query_handler(subscribe, state=RegisterForm.subscibe)
	dp.register_callback_query_handler(subscribe2, state=SubscribeForm.subscribe)

	dp.register_message_handler(get_content, content_types=ContentTypes.ANY, state=BroadcastForm.chat_id)
	dp.register_message_handler(get_markup, content_types=ContentTypes.ANY, state=BroadcastForm.markup)
	dp.register_callback_query_handler(yes_no, state=BroadcastForm.yes_no)
