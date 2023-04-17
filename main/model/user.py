from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from ..shared.shared import db
import datetime

USER_ID_SEQ = db.Sequence('adm_user_id_adm_user_seq')


class User(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'adm_user'

    id = db.Column(db.Integer, USER_ID_SEQ, unique=True,
                   server_default=USER_ID_SEQ.next_value())
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.Text)
    name = db.Column(db.String(100))
    email = db.Column(db.String(30))
    active = db.Column(db.Boolean, default=True)
    confirmation_code = db.Column(db.String(255))
    remember_token = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean, default=False)
    password_confirmation = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    company = db.Column(db.Integer, default=None)

    def __init__(self, username, name, email, password, confirmation_code, remember_token, password_confirmation, active):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.confirmation_code = confirmation_code
        self.remember_token = remember_token
        self.password_confirmation = password_confirmation
        self.active = active
        
