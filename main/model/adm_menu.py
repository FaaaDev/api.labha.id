from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db
import datetime

ADM_MENU_ID_SEQ = db.Sequence('adm_menu_id_adm_menu_seq')


class AdmMenu(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'adm_menu'

    id = db.Column(db.Integer, ADM_MENU_ID_SEQ, primary_key=True, server_default=ADM_MENU_ID_SEQ.next_value())
    name = db.Column(db.String)
    sequence_no = db.Column(db.SmallInteger)
    page_name = db.Column(db.String)
    note = db.Column(db.String(255))
    visible = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer)
    route_name = db.Column(db.String)
    icon_file = db.Column(db.String)
    sub_content = db.Column(db.String(1))
    open_target = db.Column(db.String(20))

    def __init__(self, name, sequence_no, page_name, note, visible, parent_id, route_name, icon_file, sub_content, open_target):
       self.name = name
       self.sequence_no = sequence_no
       self.page_name = page_name
       self.note = note
       self.visible = visible
       self.parent_id = parent_id
       self.route_name = route_name
       self.icon_file = icon_file
       self.sub_content = sub_content
       self.open_target = open_target
