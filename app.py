# from __init__ import app

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_pyfile('env.py')
CORS(app)
db = SQLAlchemy(app)
app.config['broker_url'] = 'redis://localhost:6379/0'



	