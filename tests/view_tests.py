from tests.test_framework import *

REDIRECT = 302
FOUND = 200


def logout():
    app.get('/logout')


def test_index_view_no_questions():
    """When not logged in and no questions have been asked,
    the index view should have the words 'Be the first!' and
    should have the option to log in.
    """
    page_text = app.get('/').get_data(as_text=True).lower()
    assert_in(
        'be the first!',
        page_text
    )
    assert_in(
        'log in',
        page_text
    )


def test_index_view_with_questions():
    """When questions have been asked, the questions' text should appear
    on the index view.
    """
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


def test_login_view_text():
    """The login view should not show the words "csrf token",
    even though the login form has that as a (hidden) field.
    """
    page_text = app.get('/login').get_data(as_text=True).lower()
    assert_not_in('csrf token', page_text)


def test_login_view_good_login():
    """When a user successfully logs in, they should be redirected
    to the index view.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        rv = app.post('/login', data=LOGIN_FORM_INFO)
        assert_equal(rv.status_code, REDIRECT)
        app.get('/logout')


def test_login_view_wrong_username():
    """When a user logs in with a username that does not exist
    in the database, they should be returned to the
    login view.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        rv = app.post('/login', data=LOGIN_FORM_INFO)
        assert_equal(rv.status_code, FOUND)


def test_login_view_wrong_password():
    """When the user logs in with the wrong password, they should
    be returned to the login view.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        rv = app.post('/login', data=LOGIN_FORM_WRONG_INFO)
        assert_equal(rv.status_code, FOUND)


def test_login_view_no_multiple_login():
    """If a user is already logged in, trying to
    access the login view should redirect
    them to the index view.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        app.post('/login', data=LOGIN_FORM_INFO)
        rv = app.get('/login')
        assert_equal(rv.status_code, REDIRECT)
        app.get('logout')


def test_index_view_logged_in():
    """When the user has logged in, the index view should
    display the link for them to log out.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        app.post('/login', data=LOGIN_FORM_INFO)
        rv = app.get('/')
        assert_in(
            'ask a question',
            rv.get_data(as_text=True).lower()
        )
        assert_in(
            'log out',
            rv.get_data(as_text=True).lower()
        )
        app.get('/logout')


def test_logout_view():
    """The logout view should log the user out"""
    with test_database(TEST_DB, [User, Question, Answer]):
        with kingsmoot.main.app.test_client() as tc:
            create_data()
            tc.post('/login', data=LOGIN_FORM_INFO)
            assert_true(kingsmoot.main.g.user.is_authenticated)
            tc.get('/logout')
            assert_false(kingsmoot.main.g.user.is_authenticated)


REGISTER_FORM_INFO = {
    'first_name': 'Daniel',
    'last_name': 'King',
    'email': 'daniel.oliver.king@gmail.com',
    'password': 'password',
    'password2': 'password'
}

REGISTER_FORM_WRONG_INFO = {
    'first_name': 'Daniel',
    'last_name': 'King',
    'email': 'daniel.oliver.king@gmail.com',
    'password': 'password',
    'password2': 'sdjnfkdsj'
}


def test_register_view_good_registration():
    """If the user registers properly, they should be
    redirected to the index view.
    """
    with test_database(TEST_DB, [User]):
        rv = app.post('/register', data=REGISTER_FORM_INFO)
        assert_equal(rv.status_code, REDIRECT)


def test_register_view_no_duplicate_email():
    """If a user tries to register with an email that already
    exists in the database, they should be brought back to
    the register view
    """
    with test_database(TEST_DB, [User]):
        app.post('/register', data=REGISTER_FORM_INFO)
        logout()
        rv = app.post('/register', data=REGISTER_FORM_INFO)
        assert_equal(rv.status_code, FOUND)
        logout()


def test_register_view_passwords_must_match():
    """If a user tries to register but the passwords do not match,
    they should be brought back to the register view
    """
    with test_database(TEST_DB, [User]):
        rv = app.post('/register', data=REGISTER_FORM_WRONG_INFO)
        assert_equal(rv.status_code, FOUND)
        logout()


def test_register_view_adds_user_to_database():
    """After registering, the database should contain the info
    of the user. Only one user should be created.
    """
    with test_database(TEST_DB, [User]):
        # Only one user should be created
        app.post('/register', data=REGISTER_FORM_INFO)
        users = User.select()
        assert_equal(users.count(), 1)

        # The user's info should match the register form info
        user = users.get()
        for key, val in REGISTER_FORM_INFO.items():
            assert_equal(user.__dict__[key], val)
        logout()


def test_register_view_already_logged_in():
    """If the user is already logged in, the register view should
    redirect them to the index view.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        app.post('/login', data=LOGIN_FORM_INFO)
        rv = app.get('/register')
        assert_equal(rv.status_code, REDIRECT)
        logout()


def test_register_view_text():
    """The register view should not have the words
    "csrf token" displayed
    """
    page_text = app.get('/register').get_data(as_text=True).lower()
    assert_not_in('csrf token', page_text)


def test_register_view_logs_user_in():
    """If the user successfully registers, they should be logged in.
    """
    with test_database(TEST_DB, [User]):
        app.post('/register', data=REGISTER_FORM_INFO)
        rv = app.get('/')
        assert_in(
            'log out',
            rv.get_data(as_text=True).lower()
        )


def test_view_question_view_contains_answers():
    """The view_question view should show all of the
    existing answers to the given question.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        question = Question.get()
        rv = app.get('/view_question/{}'.format(question.id))
        for answer in question.answers:
            assert_in(
                answer.text,
                rv.get_data(as_text=True)
            )


def test_view_question_view_contains_new_answer_form():
    """The view_question view should have a place for the user
    to type a new answer to the question
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        question = Question.get()
        rv = app.get('/view_question/{}'.format(question.id))
        assert_in(
            'Answer this question...',
            rv.get_data(as_text=True)
        )


