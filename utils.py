import asyncio
from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from create import bot, dp
from db import User
from fsm import FSMDate


async def send_reminder(dp):
	"""Функция для отправки напоминания."""
	# Циклом проходимся по всем пользователям и делаем рассылку.
	tg_id_list = User.get_tg_id_list()
	
	for tg_id in tg_id_list:
		await dp.current_state(chat=tg_id, user=tg_id).set_state(FSMDate.date)
		await bot.send_message(tg_id, text='Введите новое расписание:')


@dp.message_handler(state=FSMDate.date)
async def get_date(message: Message, state: FSMContext):
	async with state.proxy() as data:
		data['date'] = message.text
		User.update_date(message.from_user.id, data['date'])
	await state.finish()
	await message.answer('Спасибо за заполнение.')


async def check_reminder():
	"""Функция для проверки дня. Если пятница, то делаем рассылку."""
	current_day = datetime.now().strftime("%A")
	current_hour = datetime.now().hour
	if current_day == 'Friday':
		if current_hour == 10:
			await send_reminder(dp)


async def scheduler():
	"""Запускает функцию проверки дня."""
	while True:
		await check_reminder()
		# Проверка каждую минуту
		await asyncio.sleep(3590)
