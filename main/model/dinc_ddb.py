from main.shared.shared import db


class IncDdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'INCDDB'

    id = db.Column(db.Integer, primary_key=True)
    inc_id = db.Column(db.Integer)
    acc_code = db.Column(db.Integer)
    dbcr = db.Column(db.Boolean)
    value = db.Column(db.Integer)
    desc = db.Column(db.Text)

    def __init__(self, inc_id, acc_code, dbcr, value, desc):
        self.inc_id = inc_id
        self.acc_code = acc_code
        self.dbcr = dbcr
        self.value = value
        self.desc = desc
        
