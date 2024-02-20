import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import Location


def kb_for_date_select_for_update():
	"""Клавиатура для выбора даты."""
	# Определяем текущую дату.
	today = datetime.date.today()

	# Создаем список дат для следующей модели.
	next_week_dates = [today + datetime.timedelta(days=i) for i in range(10)][3:]

	# Создаем inline клавиатуру
	date_kb = InlineKeyboardMarkup(row_width=1)
	for date in next_week_dates:
		button_text = date.strftime('%d.%m.%y')  # Форматируем дату в строку 'день.месяц'
		callback_data = f'select_update_date_{date.day}_{date.month}_{date.year}'
		date_kb.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

	return date_kb


def kb_for_date_select():
	"""Клавиатура для выбора даты."""
	# Определяем текущую дату.
	today = datetime.date.today()

	# Создаем список дат для следующей модели.
	next_week_dates = [today + datetime.timedelta(days=i) for i in range(10)][3:]

	# Создаем inline клавиатуру
	date_kb = InlineKeyboardMarkup(row_width=1)
	for date in next_week_dates:
		button_text = date.strftime('%d.%m.%y')  # Форматируем дату в строку 'день.месяц'
		callback_data = f'select_date_{date.day}_{date.month}_{date.year}'
		date_kb.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

	return date_kb


def kb_for_time_select():
	"""Клавиатура для выбора времени."""
	morn = InlineKeyboardButton(text="Утро", callback_data="select_time_Утро")
	daytime = InlineKeyboardButton(text="День", callback_data="select_time_День")
	nighttime = InlineKeyboardButton(text="Ночь", callback_data="select_time_Ночь")

	time_kb = InlineKeyboardMarkup().add(morn).add(daytime).add(nighttime)

	return time_kb


def kb_for_loc_select():
	"""Клавиатура для выбора локации."""
	num_loc = Location.get_num_loc()
	loc_kb = InlineKeyboardMarkup()

	for i in range(num_loc):
		button_text = f"Room {i+1}"
		callback_data = f'create_kb_{button_text}'
		loc_kb.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

	return loc_kb


def kb_for_location():
	"""Клавиатура, генерирующая кнопки локации."""
	change_num = InlineKeyboardButton(text="Изменить количество локации", callback_data="change_num_loc")

	loc_kb = InlineKeyboardMarkup().add(change_num)

	return loc_kb