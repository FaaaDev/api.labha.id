from ..shared.shared import db

class UserMenu(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'user_menu'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer)
    view = db.Column(db.Boolean, default= False)
    edit = db.Column(db.Boolean, default= False)
    delete = db.Column(db.Boolean, default= False)

    def __init__(self, user_id, menu_id, view, edit, delete):
       self.user_id = user_id
       self.menu_id = menu_id
       self.view = view
       self.edit = edit
       self.delete = delete
