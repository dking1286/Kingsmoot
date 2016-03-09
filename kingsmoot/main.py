from flask import Flask, g, render_template
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
from flask_bcrypt import check_password_hash

from kingsmoot.models import (init_db, User, Question,
                              Answer, DoesNotExist, DB)
from kingsmoot.forms import RegisterForm

app = Flask(__name__)
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


@app.route('/register')
def register():
    form = RegisterForm()


@app.route('/login')
def login():
    pass


@app.route('/logout')
@login_required
def logout():
    pass


@app.route('/')
def index():
    """Home page question stream"""
    questions = Question.select().order_by(Question.timestamp).limit(10)
    inputs = {
        'questions': questions
    }
    return render_template('index.html', **inputs)


@app.route('/view_question/<question_id>')
@login_required
def view_question(question_id):
    pass


@app.route('/new_question')
@login_required
def new_question():
    pass


if __name__ == '__main__':
    init_db()
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )

