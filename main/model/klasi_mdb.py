from flask_sqlalchemy import SQLAlchemy
from ..shared.shared import db

class KlasiMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'KLASIMDB'

    id = db.Column(db.Integer, primary_key=True)
    klasiname = db.Column(db.String(100))
    

    def __init__(self, name):
        self.klasiname = name