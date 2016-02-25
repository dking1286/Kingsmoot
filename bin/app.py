from flask import Flask, g
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
from flask_bcrypt import check_password_hash

import kingsmoot.models as models

app = Flask(__name__)
app.secret_key = 'sljdnfohr80wnfskjdnf9283rnkwjndf982rknjdsn9f8wrkn:woenf082'

run_context = {
    'debug': True,
    'port': 8000,
    'host': '0.0.0.0'
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database prior to each request"""
    g.db = models.DB
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database after each request"""
    g.db.close()
    return response


if __name__ == '__main__':
    app.run(**run_context)

