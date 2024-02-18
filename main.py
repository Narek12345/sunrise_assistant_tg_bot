import asyncio
from datetime import datetime

from aiogram import executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from utils import scheduler
from create import bot, dp
from db import Base, engine, User
from fsm import FSMData


@dp.message_handler(commands=['start'], state=None)
async def start_cmd(message: Message):
	tg_id = message.from_user.id
	# Регистрируем пользователя, если он еще не зарегестрирован.
	User.register(tg_id, message.from_user.username)
	# Проверяем, вводил ли этот пользователь данные или нет.
	check = User.check(tg_id)

	if not check:
		# Не заполнил. Просим заполнить. FSM.
		await FSMData.date.set()
		await message.answer('Введите пожалуйста расписание:')
	else:
		await message.answer('В пятницу бот попросит вас заполнить расписание.')


@dp.message_handler(state=FSMData.date)
async def get_date(message: Message, state: FSMContext):
	async with state.proxy() as data:
		data['date'] = message.text
	await FSMData.next()
	await message.answer('Введите пожалуйста локацию:')


@dp.message_handler(state=FSMData.location)
async def get_location(message: Message, state: FSMContext):
	async with state.proxy() as data:
		data['location'] = message.text
	await FSMData.next()
	await message.answer('Введите пожалуйста Д/У/Н:')


@dp.message_handler(state=FSMData.time)
async def get_location(message: Message, state: FSMContext):
	async with state.proxy() as data:
		data['time'] = message.text
		User.fill_table_with_data(message.from_user.id, data['date'], data['location'], data['time'])
	await state.finish()
	await message.answer('Спасибо за заполнение.')


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
