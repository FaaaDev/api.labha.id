from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db
import datetime



class AdmUserMenu(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'adm_user_menu'

    id_adm_user = db.Column(db.Integer, primary_key=True)
    id_adm_menu = db.Column(db.Integer, primary_key=True)
    view = db.Column(db.Boolean)
    edit = db.Column(db.Boolean)
    delete = db.Column(db.Boolean)

    def __init__(self, id_adm_user, id_adm_menu, view, edit, delete):
      self.id_adm_user = id_adm_user
      self.id_adm_menu = id_adm_menu
      self.view = view
      self.edit = edit
      self.delete = delete