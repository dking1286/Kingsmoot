from tests.test_framework import *

GOOD_STATUS = 200
BAD_STATUS = 404


@kingsmoot.main.app.route('/registerformtester', methods=['POST'])
def register_form_checker_view():
    register_form = RegisterForm()

    for field in register_form:
        if not field.validate(register_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


@kingsmoot.main.app.route('/loginformtester', methods=['POST'])
def login_form_checker_view():
    login_form = LoginForm()

    for field in login_form:
        if not field.validate(login_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


@kingsmoot.main.app.route('/newquestionformtester', methods=['POST'])
def new_question_form__checker_view():
    new_question_form = NewQuestionForm()

    for field in new_question_form:
        if not field.validate(new_question_form):
                return 'Bad', BAD_STATUS
    return 'Good', GOOD_STATUS


@kingsmoot.main.app.route('/newanswerformtester', methods=['POST'])
def new_answer_form_checker_view():
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

