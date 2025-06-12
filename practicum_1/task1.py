# Есть небольшой набор данных. Написать маршрут, который
# возвращает имя по user_id из этого набора данных и
# User not found -- если ничего не найдено.
#

from flask import Flask

app = Flask(__name__)

users = {1: "Alice", 2: "Bob", 3: "Charlie"}


@app.route('/user/<int:user_id>')
def get_user(user_id):
    name = users.get(user_id)
    if name:
        return name
    else:
        return "User not found"


if __name__ == '__main__':
    app.run()
