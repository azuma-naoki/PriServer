from flask import Flask, request, jsonify
from flask_cors import CORS
import  matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p> Welcome PriServer!</p>"

@app.route("/test", methods=['POST'])
def test():
    json = request.get_json()

    name = json['name']
    value = json['price']

    books = {'name':name, 'value':value}

    return jsonify(books)

@app.route("/print", methods=['POST'])
def write():
    json = request.get_json()

    x = json['x']
    y = json['y']

    x = np.array(x, dtype=np.uint8)
    y = np.array(y, dtype=np.uint8)

    plt.plot(x, y)

    ofs = BytesIO()
    plt.savefig(ofs, format="jpg")
    png_data = ofs.getvalue()
    plt.close()

    base64_data = base64.b64encode(png_data).decode()

    data = {"value":base64_data}

    return jsonify(data)
