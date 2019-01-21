from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = './base.db' 
from views import *


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')

