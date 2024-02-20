import asyncio
from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from utils import scheduler
from create import bot, dp
from db import Base, engine, User, Location
from fsm import FSMData, FSMLocation, FSMDate
from keyboards import kb_for_date_select, kb_for_time_select, kb_for_location, kb_for_loc_select
from config import ADMIN_ID


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
		await message.answer('Выберите дату:', reply_markup=kb_for_date_select())
	else:
		await message.answer('В пятницу бот попросит вас заполнить дату.')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('select_date'), state=FSMData.date)
async def process_callback_1(callback_query: CallbackQuery, state: FSMContext):
	date = callback_query.data.split('_')[2] + '.' + callback_query.data.split('_')[3] + '.' + callback_query.data.split('_')[4]
	async with state.proxy() as data:
		data['date'] = date
	await FSMData.next()
	await callback_query.message.answer('Выберите локацию:', reply_markup=kb_for_loc_select())
	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('create_kb'), state=FSMData.location)
async def process_callback_2(callback_query: CallbackQuery, state: FSMContext):
	location = callback_query.data.split('_')[2]
	async with state.proxy() as data:
		data['location'] = location
	await FSMData.next()
	await callback_query.message.answer('Выберите время суток (Утро, День, Ночь):', reply_markup=kb_for_time_select())
	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('select_time'), state=FSMData.time)
async def process_callback_3(callback_query: CallbackQuery, state: FSMContext):
	time = callback_query.data.split('_')[2]
	async with state.proxy() as data:
		data['time'] = time
		User.fill_table_with_data(callback_query.from_user.id, data['date'], data['location'], data['time'])
	await state.finish()
	await callback_query.message.answer('Данные сохранены✅')
	await bot.answer_callback_query(callback_query.id)


@dp.message_handler(commands='to_admin')
async def start_cmd(message: Message):
	if message.from_user.id != ADMIN_ID:
		await message.answer('Вы не являетесь админом!')
	else:
		await message.answer('Добро пожаловать в панель администратора.', reply_markup=kb_for_location())


@dp.callback_query_handler(text="change_num_loc", state=None)
async def change_num_loc_call(callback_query: CallbackQuery):
	await FSMLocation.loc.set()
	await callback_query.message.answer('Введите новое количество локации (только числа, без букв и знаков):')
	await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=FSMLocation.loc)
async def get_location(message: Message, state: FSMContext):
	text = message.text
	try:
		text = int(text)
		if text <= 0:
			await message.answer('Нельзя вводить 0 или отрицательное число!')
		else:
			# Запрос в БД на обновление данных.
			Location.update_loc(text)
			await message.answer('Данные сохранены✅')
	except Exception as e:
		await message.answer('Вы ввели не число. Попробуйте еще раз!')
	await state.finish()


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
	# Создаем обьект Location.
	Location.create()
	asyncio.run(main())
