from nose.tools import *
from peewee import *
from playhouse.test_utils import test_database

from kingsmoot.forms import (RegisterForm, LoginForm,
                             NewQuestionForm, NewAnswerForm, ValidationError)
from kingsmoot.models import User
import kingsmoot.main

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([User], safe=True)


app = kingsmoot.main.app.test_client()


def create_users(count=2):
    for i in range(count):
        User.add(
            email='test_{}@example.com'.format(i),
            first_name='test_{}'.format(i),
            last_name='test_{}'.format(i),
            password='password'
        )


def set_up():
    kingsmoot.main.app.config['TESTING'] = True
    kingsmoot.main.app.config['WTF_CSRF_ENABLED'] = False


@kingsmoot.main.app.route('/registerformtester', methods=['POST'])
def register_form_route():
    register_form = RegisterForm()

    for field in register_form:
        if not field.validate(register_form):
                return 'Bad', 404
    return 'Good', 200


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
        assert_equal(rv.status_code, 200)


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

