from DB_model import *
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_user(name, username, password, mail):
    new_user = User(name=name, username=username, password=password, mail=mail)
    session.add(new_user)
    session.commit()


def change_password(id, new_password):
    user = session.query(User).filter_by(id=id).first()
    user.password = new_password
    session.commit()


def delete_user(id):
    session.query(User).filter_by(id=id).delete()
    session.commit()


def query_all():
   users = session.query(User).all()
   return users


def query_by_id(id):
   user = session.query(User).filter_by(id=id).first()
   return user


def query_id_by_username(username):
  user = session.query(User).filter_by(username=username).first()
  return user.id


def existed_user(username, password):
  users = [(user.username, user.password) for user in query_all()]
  return (username, password) in users


def username_exists(username):
  usernames = [user.username for user in query_all()]
  return username in usernames


def query_all_messages():
   messages = session.query(Message).all()
   return messages


def message_exists(headline, publisher_id):
  messages = []
  for message in query_all_messages():
    messages.append((message.headline, message.publisher_id))
  return (headline, publisher_id) in messages


def add_message(headline, content, publisher_name, publisher_id):
    new_message = Message(headline = headline, content = content, publisher_name = publisher_name, publisher_id = publisher_id, time = datetime.datetime.now().strftime("%c"))
    session.add(new_message)
    session.commit()
