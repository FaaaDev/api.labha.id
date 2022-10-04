from unicodedata import category
from main.shared.shared import db

class MainMenu(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'main_menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    visible = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer)
    route_name = db.Column(db.String)
    icon_file = db.Column(db.String)
    category = db.Column(db.Integer)

    def __init__(self, name, visible, parent_id, route_name, icon_file, category):
       self.name = name
       self.visible = visible
       self.parent_id = parent_id
       self.route_name = route_name
       self.icon_file = icon_file
       self.category = category
