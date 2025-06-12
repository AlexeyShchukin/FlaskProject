# Фильтрация списка по query params
# ТЗ: GET /products
# В products лежит список словарей.
# Поддерживаются query-параметры: min_price, max_price, category.
# Нужно реализовать получение записей по фильтрам церез query params

from flask import Flask, request,jsonify

app = Flask(__name__)

products = [
{"id": 1, "name": "Chair", "price": 45, "category": "furniture"},
{"id": 2, "name": "Sofa", "price": 120, "category": "furniture"},
{"id": 3, "name": "Laptop", "price": 1000, "category": "electronics"}
]


@app.route("/products")
def get_products():
    min_price = request.args.get("min_price", type=int)
    max_price = request.args.get("max_price", type=int)
    category = request.args.get("category", type=str)
    return jsonify(
        [product for product in products if min_price <= product["price"] <= max_price and product["category"] == category]
    )

if __name__ == '__main__':
    app.run()