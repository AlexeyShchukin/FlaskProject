# Написать маршрут, который будет принимать роль и действие и возвращать
# True/False по permissions.

from flask import Flask

app = Flask(__name__)

permissions = {
    "admin": ["create", "delete", "update"],
    "editor": ["update"],
    "user": ["read"]
}


# @app.route('/protected/<string:role>/<string:action>')
# def check_permissions(role, action):
#     if role in permissions and action in permissions[role]:
#         return {"allowed": True}
#     return {"allowed": False}


@app.route("/protected/<string:role>/<string:action>")
def protected(role, action):
    actions = permissions.get(role, [])
    return {"allowed": action in actions}


if __name__ == '__main__':
    app.run()
