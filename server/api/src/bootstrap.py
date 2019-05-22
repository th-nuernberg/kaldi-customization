from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://api:api-server-password@db:3306/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from db import *

import redis
redis_conn = redis.Redis(host='redis', port=6379, password='kalditproject')