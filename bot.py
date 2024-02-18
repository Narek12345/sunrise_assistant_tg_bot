import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def send_reminder():
	# Ваш код для отправки напоминания
	print('Send message')


async def check_reminder():
	current_day = datetime.now().strftime("%A")
	if current_day == 'Friday':
		await send_reminder()


async def scheduler():
	while True:
		await check_reminder()
		await asyncio.sleep(60)  # Проверка каждую минуту


@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
	await message.answer('Привет, как дела')



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
	asyncio.run(main())
