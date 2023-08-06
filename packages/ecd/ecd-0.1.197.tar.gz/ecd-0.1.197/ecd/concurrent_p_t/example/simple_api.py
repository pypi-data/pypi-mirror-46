# coding:utf-8
"""
author: Allen
datetime: 
python version: 3.x
summary: 
install package:
"""
import datetime

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/', methods=["POST"])
def index():
    resp = {"status": "ok", "data": str(datetime.datetime.now()) + '____' + request.json.get("data", "None")}
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
