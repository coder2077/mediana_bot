import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot import Config
from tgbot.config import make_db_uri
from tgbot.models.base import metadata
from tgbot.commands import register_commands
from tgbot.messages import register_messages
from tgbot.callbacks import register_callbacks
from tgbot.states import register_states
from tgbot.middlewares.db import DbSessionMiddleware



logger = logging.getLogger(__name__)

async def main():
	engine = create_async_engine(
		make_db_uri(), future=True, echo=False
	)
	session_fabric = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
	async with engine.begin() as conn:
		# await conn.run_sync(metadata.drop_all)
		await conn.run_sync(metadata.create_all)

	storage = MemoryStorage()
	bot = Bot(token=Config.tgbot.token, parse_mode='Markdown')
	dp = Dispatcher(bot, storage=storage)

	dp.middleware.setup(DbSessionMiddleware(session_fabric))

	register_commands(dp=dp)
	register_states(dp=dp)
	register_messages(dp=dp)
	register_callbacks(dp=dp)

	try:
		await dp.skip_updates()
		await dp.start_polling()
	finally:
		await dp.storage.close()
		await dp.storage.wait_closed()
		await bot.session.close()


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except (KeyboardInterrupt, SystemExit):
		logger.error("Bot stopped!")
