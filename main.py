import asyncio
from datetime import datetime

from aiogram.types import Message

from config import API_TOKEN
from utils import scheduler
from create imprt bot, dp


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
