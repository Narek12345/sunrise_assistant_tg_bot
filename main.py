import asyncio
from datetime import datetime

from aiogram import executor
from aiogram.types import Message

from utils import scheduler
from create import bot, dp
from db import Base, engine, User


@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
	# Регистрируем пользователя, если он еще не зарегестрирован.
	register = User.register(message.from_user.id, message.from_user.username)

	if register:
		# Зарегестрирован.
		print('зарегестрирован')
	else:
		# Не зарегестрирован.
		# Просим заполнить данные.
		print('Заполни данные')


async def main():
	loop = asyncio.get_event_loop()
	loop.create_task(scheduler())
	await dp.start_polling(bot)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		loop.stop()
		tasks = asyncio.all_tasks(loop)
		for task in tasks:
			task.cancel()
			with suppress(asyncio.CancelledError):
				loop.run_until_complete(task)


if __name__ == '__main__':
	# Регистрируем БД.
	Base.metadata.create_all(bind=engine)
	asyncio.run(main())
