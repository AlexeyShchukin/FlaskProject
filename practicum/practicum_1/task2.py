from flask import Flask

app = Flask(__name__)

data = ["apple", "banana", "cherry"]

@app.route('/fruits/<string:name>', methods=['DELETE'])
def delete_item(name):
    if name in data:
        data.remove(name)
        return {"message": "Item successfully deleted"}, 204
    else:
        return {"massage": "Item not found"}, 404


if __name__ == '__main__':
    app.run()