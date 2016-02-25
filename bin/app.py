from flask import Flask

app = Flask(__name__)
app.secret_key = 'sljdnfohr80wnfskjdnf9283rnkwjndf982rknjdsn9f8wrkn:woenf082'

run_context = {
    'debug': True,
    'port': 8000,
    'host': '0.0.0.0'
}


@app.route('/')
def index():
    return "Hello world!"


if __name__ == '__main__':
    app.run(**run_context)

