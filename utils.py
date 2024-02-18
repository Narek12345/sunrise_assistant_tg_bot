import asyncio
from datetime import datetime

from create import bot


async def send_reminder():
	"""Функция для отправки напоминания."""
	# Циклом проходимся по всем пользователям и делаем рассылку.
	pass


async def check_reminder():
	"""Функция для проверки дня. Если пятница, то делаем рассылку."""
	current_day = datetime.now().strftime("%A")
	current_hour = datetime.now().hour
	if current_day == 'Friday':
		if current_hour == 10:
			await send_reminder()


async def scheduler():
	"""Запускает функцию проверки дня."""
	while True:
		await check_reminder()
		# Проверка каждую минуту
		await asyncio.sleep(2400)
