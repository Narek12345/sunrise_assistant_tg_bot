import asyncio
from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from create import bot, dp
from db import User
from fsm import FSMDate
from keyboards import kb_for_date_select_for_update


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('select_update_date'), state=FSMDate.date)
async def process_callback_5(callback_query: CallbackQuery, state: FSMContext):
	date = callback_query.data.split('_')[3] + '.' + callback_query.data.split('_')[4] + '.' + callback_query.data.split('_')[5]
	async with state.proxy() as data:
		data['date'] = date
		User.update_date(callback_query.from_user.id, data['date'])
	await state.finish()
	await callback_query.message.answer('Данные сохранены✅')
	await bot.answer_callback_query(callback_query.id)


async def send_reminder(dp):
	"""Функция для отправки напоминания."""
	# Циклом проходимся по всем пользователям и делаем рассылку.
	tg_id_list = User.get_tg_id_list()
	
	for tg_id in tg_id_list:
		await dp.current_state(chat=tg_id, user=tg_id).set_state(FSMDate.date)
		await bot.send_message(tg_id, 'Выберите новую дату:', reply_markup=kb_for_date_select_for_update())


async def check_reminder():
	"""Функция для проверки дня. Если пятница, то делаем рассылку."""
	current_day = datetime.now().strftime("%A")
	current_hour = datetime.now().hour
	current_minute = datetime.now().minute
	if current_day == 'Tuesday': # Friday
		if current_hour == 19: # 10
			if current_minute == 21: # 10
				await send_reminder(dp)


async def scheduler():
	"""Запускает функцию проверки дня."""
	while True:
		# Задерживаем.
		await asyncio.sleep(25)
		await check_reminder()
		# Проверка каждую минуту
		await asyncio.sleep(40)
