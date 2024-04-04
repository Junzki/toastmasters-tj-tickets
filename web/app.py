# -*- coding: utf-8 -*-
from flask import Flask, render_template

from concurrent.futures.thread import ThreadPoolExecutor

app = Flask(__name__)

app.config.from_object('common.settings.settings')



@app.route('/')
def index():
    return render_template('index.html')
