from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	username = Column(String)
	password = Column(String)
	mail = Column(String)


class Message(Base):
	__tablename__ = 'messages'
	id = Column(Integer, primary_key=True)
	headline = Column(String)
	content = Column(String)
	publisher_name = Column(String)
	publisher_id = Column(Integer)
	time = Column(String)
