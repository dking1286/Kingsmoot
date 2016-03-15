from tests.test_framework import *


def test_index_view_no_questions():
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
    page_text = app.get('/login').get_data(as_text=True).lower()
    assert_not_in(
        'csrf token',
        page_text
    )


def test_login_view_good_login():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        rv = app.post('/login', data=LOGIN_FORM_INFO)
        assert_equal(rv.status_code, 302)
        app.get('/logout')


def test_login_view_wrong_username():
    with test_database(TEST_DB, [User, Question, Answer]):
        rv = app.post('/login', data=LOGIN_FORM_INFO)
        assert_equal(rv.status_code, 200)


def test_login_view_wrong_password():
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        rv = app.post('/login', data=LOGIN_FORM_WRONG_INFO)
        assert_equal(rv.status_code, 200)


def test_login_view_no_multiple_login():
    """If a user is already logged in, the login view should redirect
    them to the index view.
    """
    with test_database(TEST_DB, [User, Question, Answer]):
        create_data()
        app.post('/login', data=LOGIN_FORM_INFO)
        rv = app.get('/login')
        assert_equal(rv.status_code, 302)
        app.get('logout')


def test_index_view_logged_in():
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
