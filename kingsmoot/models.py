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
    first_name = CharField()
    last_name = CharField()
    join_date = DateField(default=datetime.date.today)
    password = CharField(max_length=100)

    @classmethod
    def add(cls, email, first_name, last_name, password):
        try:
            with DB.transaction():
                cls.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User with that email already exists")


class Question(BaseModel):
    id = PrimaryKeyField()
    text = TextField()
    user = ForeignKeyField(User, related_name='questions')
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def add(cls, text, user):
        cls.create(
            text=text,
            user=user
        )


class Answer(BaseModel):
    text = TextField()
    user = ForeignKeyField(User, related_name='answers')
    question = ForeignKeyField(Question, related_name='answers')
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def add(cls, text, user, question):
        cls.create(
            text=text,
            user=user,
            question=question
        )


def init_db():
    """Initialize the database"""
    DB.connect()
    DB.create_tables([User, Question, Answer], safe=True)
    DB.close()
