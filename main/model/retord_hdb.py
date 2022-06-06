from main.shared.shared import db


class RetordHdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'RETORDHDB'

    id = db.Column(db.Integer, primary_key=True)
    ret_code = db.Column(db.String(255), unique=True)
    ret_date = db.Column(db.TIMESTAMP)
    fk_id = db.Column(db.Integer)

    def __init__(self, ret_code, ret_date, fk_id):
        self.ret_code = ret_code
        self.ret_date = ret_date
        self.fk_id = fk_id
        