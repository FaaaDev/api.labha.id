from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db =  SQLAlchemy()
ma = Marshmallow()
server_name = "http://192.168.0.100:5001"