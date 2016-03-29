from flask import (Flask, g, render_template, request, redirect,
                   url_for, flash)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from flask_bcrypt import check_password_hash

from kingsmoot.models import (init_db, User, Question,
                              Answer, DoesNotExist, DB)
from kingsmoot.forms import (RegisterForm, LoginForm, NewAnswerForm,
                             NewQuestionForm)

app = Flask('kingsmoot')
app.secret_key = 'sljdnfohr80wnfskjdnf9283rnkwjndf982rknjdsn9f8wrkn:woenf082'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database prior to each request"""
    g.db = DB
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database after each request"""
    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    success_message = "Congratulations, you have been registered!"

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST' and form.validate():
        User.add(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data
        )
        user = User.get(User.email == form.email.data)
        login_user(user)
        flash(success_message, 'success')
        return redirect(url_for('index'))

    return render_template(
        'register.html',
        form=form
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    failure_message = "Incorrect username or password"
    success_message = "You have successfully logged in!"

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST' and form.validate():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash(failure_message, "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(success_message, 'success')
                return redirect(url_for('index'))
            else:
                flash(failure_message, "error")

    return render_template(
        'login.html',
        form=form
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out. Come back soon!")
    return redirect(url_for('login'))


@app.route('/')
def index():
    """Home page question stream"""
    questions = Question.select().order_by(Question.timestamp).limit(10)
    return render_template(
        'index.html',
        questions=questions
    )


@app.route('/view_question/<question_id>', methods=['GET', 'POST'])
@login_required
def view_question(question_id):
    form = NewAnswerForm()
    question = Question.get(Question.id == question_id)
    success_message = 'Your answer has been posted!'

    if request.method == 'POST' and form.validate():
        Answer.add(
            text=form.text.data,
            question=question,
            user=current_user._get_current_object()
        )
        flash(success_message, 'success')

    return render_template(
        'view_question.html',
        question=question,
        form=form
    )


@app.route('/new_question', methods=['GET', 'POST'])
@login_required
def new_question():
    form = NewQuestionForm()
    success_message = 'Your question has been posted!'

    if request.method == 'POST' and form.validate():
        Question.add(
            text=form.text.data,
            user=current_user._get_current_object()
        )
        flash(success_message, 'success')
        return redirect(url_for('index'))

    return render_template(
        'new_question.html',
        form=form
    )


if __name__ == '__main__':
    init_db()
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )

