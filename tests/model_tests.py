from tests.test_framework import *


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
