from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Hello, Flask!"


@app.route("/user/<string:name>")
def get_user_by_id(name):
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run()
