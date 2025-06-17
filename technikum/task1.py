#  Implementierung einer dynamischen Route /api/v1/<path:filepath> in Flask
# Ziel: Eine API-Endpunkt soll einen dynamischen Pfad akzeptieren und als JSON zurückgeben.
# Frage: Welche anderen Typisierer für Endpunkte haben Sie sich gemerkt?
import json
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)

filepath = Path(__file__).parent.parent.joinpath('file.json')


@app.route('/api/v1/<path:filepath>', methods=['GET'])
def home(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
