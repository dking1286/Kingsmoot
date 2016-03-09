Kingsmoot, a miniature forum app

Author: Daniel King

Design narration:

I want to design a website where people can ask and get answers to each others' questions.

People should be able to register for an account using their email address, and then once they log in,
they should be able to view a stream of recent questions that have been asked. They can click on a question and read
all of the answers that have been posted so far, and they can post their own answer if they like. Or, on the question
stream page, there should be a button that allows them to post a new question.

When viewing the question stream, each question should be labeled with the user that posted it, as well as the timestamp.
Similarly, when viewing the answers to a given question, each answer should be labeled with the user's name who posted it.

In the next version, question should be indexed to a given subject, and people can follow subjects. Then, when they are on the
stream page, by default they see questions that relate only to the subjects they are following. However, maybe there is a button
that allows them to view a stream of questions from any subject. Maybe a dropdown menu where they can choose the subject they would like to view.

Models:
  User
    email
    first_name
    last_name
    join_date
    password
  Question
    text
    user
    timestamp
  Answer
    text
    user
    question
    timestamp

Forms:
  login_form
    email
    password
  register_form
    email
    first_name
    last_name
  new_question_form
    text
  new_answer_form
    text

Views:
  login
  logout
  register
  index (stream)
  new_question
  view_question (allows to input a new answer)


