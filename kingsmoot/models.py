import os.path
import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

db_name = 'kingsmoot_data.db'
directory = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(directory, db_name)

DB = SqliteDatabase(full_path)


class BaseModel(Model):
    class Meta:
        database = DB


class User(BaseModel, UserMixin):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    @classmethod
    def securely_create(cls, email, password):
        try:
            with DB.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User with that email already exists")


class Question(BaseModel):
    text = TextField()
    user = ForeignKeyField(User, related_name='questions')
    subject = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)


class Answer(BaseModel):
    text = TextField()
    user = ForeignKeyField(User, related_name='answers')
    question = ForeignKeyField(Question, related_name='answers')
    timestamp = DateTimeField(default=datetime.datetime.now)
