from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///db.db')
Session = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
	pass


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	tg_id = Column(Integer)
	tg_username = Column(String)
	date = Column(String)
	location = Column(String)
	time = Column(String)


	def register(tg_id, tg_username):
		"""Регистрируем пользователя, если он еще не зарегестрирован."""
		with Session(autoflush=False, bind=engine) as db:
			user = db.query(User).filter(User.tg_id==tg_id).first()

			if user == None:
				new_user = User(tg_id=tg_id, tg_username=tg_username, date='', location='', time='')
				db.add(new_user)
				db.commit()

				print(new_user.date)
				print(type(new_user.date))

				return True
			return False


	def fill_table_with_data(tg_id, date, location, time):
		"""Заполняем данными таблицу."""
		pass


	def check(tg_id):
		"""Проверяем, заполнил ли пользователь таблицу данными."""
		with Session(autoflush=False, bind=engine) as db:
			user = db.query(User).filter(User.tg_id==tg_id).first()

			if user.date=='' or user.location=='' or user.time=='':
				# Не заполнил.
				return False
			return True

