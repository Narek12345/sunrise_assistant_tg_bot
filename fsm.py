from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMData(StatesGroup):
	date = State()
	location = State()
	time = State()


class FSMDate(StatesGroup):
	date = State()
