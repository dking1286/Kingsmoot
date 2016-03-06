from nose.tools import *
from peewee import *
from playhouse.test_utils import test_database

from kingsmoot.forms import (RegisterForm, LoginForm,
                             NewQuestionForm, NewAnswerForm)
from kingsmoot.models import User, Question, Answer
import kingsmoot.main

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()

app = kingsmoot.main.app.test_client()


# Helper functions #################
def create_users(count=2):
    for i in range(count):
        User.add(
            email='test_{}@example.com'.format(i),
            first_name='test_{}'.format(i),
            last_name='test_{}'.format(i),
            password='password'
        )


def create_data(count=2):
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
        for question in questions:
            Answer.add(
                text="text",
                user=user,
                question=question
            )


# Set up #########################
def set_up():
    kingsmoot.main.app.config['TESTING'] = True
    kingsmoot.main.app.config['WTF_CSRF_ENABLED'] = False

GOOD_STATUS = 200
BAD_STATUS = 404


# Form tests ####################
@kingsmoot.main.app.route('/registerformtester', methods=['POST'])
def register_form_view():
    register_form = RegisterForm()

    for field in register_form:
        if not field.validate(register_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


@kingsmoot.main.app.route('/loginformtester', methods=['POST'])
def login_form_view():
    login_form = LoginForm()

    for field in login_form:
        if not field.validate(login_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


@kingsmoot.main.app.route('/newquestionformtester', methods=['POST'])
def new_question_form_view():
    new_question_form = NewQuestionForm()

    for field in new_question_form:
        if not field.validate(new_question_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


@kingsmoot.main.app.route('/newanswerformtester', methods=['POST'])
def new_answer_form_view():
    new_answer_form = NewAnswerForm()

    for field in new_answer_form:
        if not field.validate(new_answer_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


def test_register_form_valid():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'testform@test.com',
            'password': 'hithere',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, GOOD_STATUS)


def test_register_form_missing_first_name():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': '',
            'last_name': 'King',
            'email': 'testform@test.com',
            'password': 'hithere',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_missing_last_name():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': '',
            'email': 'testform@test.com',
            'password': 'hithere',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_missing_email():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': '',
            'password': 'hithere',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_invalid_email():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'testform',
            'password': 'hithere',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_email_exists():
    with test_database(TEST_DB, [User]):
        create_users()
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'test_1@example.com',
            'password': 'hithere',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_missing_password1():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'testform@test.com',
            'password': '',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_too_short_password1():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'testform@test.com',
            'password': 'h',
            'password2': 'h',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_wrong_password1():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'testform@test.com',
            'password': 'hi',
            'password2': 'hithere',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_register_form_missing_password2():
    with test_database(TEST_DB, [User]):
        test_data = {
            'first_name': 'Daniel',
            'last_name': 'King',
            'email': 'testform@test.com',
            'password': 'hithere',
            'password2': '',
            'csrf_token': 'secret'
        }
        rv = app.post(
            '/registerformtester',
            data=test_data
        )
        assert_equal(rv.status_code, 404)


def test_login_form_valid():
    test_data = {
        'email': 'test@example.com',
        'password': 'password'
    }
    rv = app.post(
        '/loginformtester',
        data=test_data
    )
    assert_equal(rv.status_code, GOOD_STATUS)


def test_login_form_missing_email():
    test_data = {
        'email': '',
        'password': 'password'
    }
    rv = app.post(
        '/loginformtester',
        data=test_data
    )
    assert_equal(rv.status_code, BAD_STATUS)


def test_login_form_invalid_email():
    test_data = {
        'email': 'test',
        'password': 'password'
    }
    rv = app.post(
        '/loginformtester',
        data=test_data
    )
    assert_equal(rv.status_code, BAD_STATUS)


def test_login_form_missing_password():
    test_data = {
        'email': 'test@example.com',
        'password': ''
    }
    rv = app.post(
        '/loginformtester',
        data=test_data
    )
    assert_equal(rv.status_code, BAD_STATUS)


def test_new_question_form_valid():
    test_data = {
        'text': 'Why is the sky?'
    }
    rv = app.post(
        '/newquestionformtester',
        data=test_data
    )
    assert_equal(rv.status_code, GOOD_STATUS)


def test_new_question_form_missing_text():
    test_data = {
        'text': ''
    }
    rv = app.post(
        '/newquestionformtester',
        data=test_data
    )
    assert_equal(rv.status_code, BAD_STATUS)


def test_new_answer_form_valid():
    test_data = {
        'text': 'Because.'
    }
    rv = app.post(
        '/newanswerformtester',
        data=test_data
    )
    assert_equal(rv.status_code, GOOD_STATUS)


def test_new_answer_form_missing_text():
    test_data = {
        'text': ''
    }
    rv = app.post(
        '/newanswerformtester',
        data=test_data
    )
    assert_equal(rv.status_code, BAD_STATUS)


# Model tests ###########################
def test_user_creation():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        user = User.select().where(User.first_name == 'test_0').get()
        assert_equal(user.email, 'test_0@example.com')


def test_no_duplicate_email():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        user_info = {
            'email': 'test_0@example.com',
            'first_name': 'Daniel',
            'last_name': 'King',
            'password': 'password'
        }
        assert_raises(ValueError, User.add, **user_info)
