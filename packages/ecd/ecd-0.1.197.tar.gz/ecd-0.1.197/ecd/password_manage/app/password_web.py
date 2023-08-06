# coding:utf-8
"""
@author:ZouLingyun
@date:
@summary:
"""
import time

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from ecd.password_manage.app.handle_data import HandleData

hd = HandleData()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/suggest/')
def password():
    keyword = request.args.get('keyword', None)
    hits = hd.search(keyword, 20)
    return jsonify(hits)


if __name__ == '__main__':
    pass
