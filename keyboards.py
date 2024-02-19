from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_for_date_select():
	"""Клавиатура для выбора даты."""
	pass


def kb_for_time_select():
	"""Клавиатура для выбора времени."""
	morn = InlineKeyboardButton(text="Утро", callback_data="select_time_Утро")
	daytime = InlineKeyboardButton(text="День", callback_data="select_time_День")
	nighttime = InlineKeyboardButton(text="Ночь", callback_data="select_time_Ночь")

	time_kb = InlineKeyboardMarkup().add(morn).add(daytime).add(nighttime)

	return time_kb