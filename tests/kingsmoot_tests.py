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
        i = user.first_name[-1]
        for question in questions:
            j, k = question.text[-3], question.text[-1]
            Answer.add(
                text="text_{}_{}_{}".format(i, j, k),
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


def test_user_no_duplicate_email():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        user_info = {
            'email': 'test_0@example.com',
            'first_name': 'Daniel',
            'last_name': 'King',
            'password': 'password'
        }
        assert_raises(ValueError, User.add, **user_info)


def test_user_automatic_join_date():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        users = User.select().where(User.join_date == datetime.date.today())
        user = users.get()
        assert_equal(users.count(), 2)
        assert_equal(user.join_date, datetime.date.today())


def test_user_password_max_length():
    with test_database(TEST_DB, [User, Question, Answer]):
        assert_raises(
            ValueError,
            User.add(
                email='test@example.com',
                first_name='Daniel',
                last_name='King',
                password='p'*101
            )
        )


def test_user_get_all_questions():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        questions = User.get(User.email == 'test_0@example.com').questions
        assert_equal(questions.count(), 2)


def test_user_get_answers():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        users = User.select()
        for user in users:
            for answer in user.answers:
                assert_equal(
                    user.first_name[-1],
                    answer.text[-5]
                )


def test_question_creation():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        questions = Question.select()
        question = questions.where(Question.text == 'text_0_0').get()
        assert_equal(questions.count(), 4)
        assert_equal(question.user.email, 'test_0@example.com')


def test_question_timestamp():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        questions = Question.select()
        for question in questions:
            assert_less(
                question.timestamp - datetime.datetime.now(),
                datetime.timedelta(1)
            )


def test_question_get_answers():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        question = Question.get(Question.text == 'text_0_0')
        for answer in question.answers:
            assert_equal(
                question.text[-3],
                answer.text[-3]
            )
            assert_equal(
                question.text[-1],
                answer.text[-1]
            )

# View tests ###########################


def test_index_view_no_questions():
    assert_in(
        'be the first!',
        app.get('/').get_data(as_text=True).lower(),
    )


def test_index_view_with_questions():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        questions = Question.select()
        for question in questions:
            assert_in(
                question.text,
                app.get('/').get_data(as_text=True)
            )


LOGIN_FORM_INFO = {
    'email': 'test_0@example.com',
    'password': 'password'
}

LOGIN_FORM_WRONG_INFO = {
    'email': 'test_0@example.com',
    'password': 'passwrd'
}


def test_login_view_good_login():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        rv = app.post('/login', data=LOGIN_FORM_INFO)
        assert_equal(rv.status_code, 302)


def test_login_view_wrong_username():
    with test_database(TEST_DB, [User, Question, Answer]):
        rv = app.post('/login', data=LOGIN_FORM_INFO)
        assert_equal(rv.status_code, 200)


def test_login_view_wrong_password():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        rv = app.post('/login', data=LOGIN_FORM_WRONG_INFO)
        assert_equal(rv.status_code, 200)


def test_index_view_logged_in():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        app.post('/login', data=LOGIN_FORM_INFO)
        rv = app.get('/')
        assert_in(
            'new question',
            rv.get_data(as_text=True).lower()
        )
        assert_in(
            'log out',
            rv.get_data(as_text=True).lower()
        )





