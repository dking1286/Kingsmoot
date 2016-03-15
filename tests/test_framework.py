import datetime

from nose.tools import *
from peewee import *
from playhouse.test_utils import test_database

from kingsmoot.forms import (RegisterForm, LoginForm,
                             NewQuestionForm, NewAnswerForm)
from kingsmoot.models import User, Question, Answer
import kingsmoot.main

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()

kingsmoot.main.app.config['TESTING'] = True
kingsmoot.main.app.config['WTF_CSRF_ENABLED'] = False

app = kingsmoot.main.app.test_client()


# Helper functions #################
def create_users(count=2):
    """Create some users in the database.

    Users will be numbered from 0 to count

    Args:
        count (int): The number of users to be created
    """
    for i in range(count):
        User.add(
            email='test_{}@example.com'.format(i),
            first_name='test_{}'.format(i),
            last_name='test_{}'.format(i),
            password='password'
        )


def create_data(count=2):
    """Create some users, questions, and answers in the database.

    Users will be numbered from 0 to count.

    "count" Questions will be created corresponding to each user.
    Each Question's text is in the form "text_i_j", where i is the
    number of the user and j is the number of the question. So,
    "text_0_1" is the text of Question 1 asked by User 0.

    Each User will have an Answer corresponding to each Question.
    Each Answer's text is in the format "text_i_j_k", where i is the
    number of the user the Answer belongs to, and j, k are the indices of
    the Question the answer is written for. So, "text_0_1_2" is the text of
    the Answer written by User 0 to answer the 2'th Question asked by User 1.

    Args:
        count (int): The number of Users to create, and the number of Questions
        to create for each User
    """
    for i in range(count):
        User.add(
            email='test_{}@example.com'.format(i),
            first_name='test_{}'.format(i),
            last_name='test_{}'.format(i),
            password='password'
        )

    users = User.select()
    for user in users:
        i = user.first_name[-1]
        for j in range(count):
            Question.add(
                text="text_{}_{}".format(i, j),
                user=user
            )

    questions = Question.select()
    for user in users:
        i = user.first_name[-1]
        for question in questions:
            j, k = question.text[-3], question.text[-1]
            Answer.add(
                text="text_{}_{}_{}".format(i, j, k),
                user=user,
                question=question
            )



