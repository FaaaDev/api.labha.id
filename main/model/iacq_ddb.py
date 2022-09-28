from main.shared.shared import db


class IAcqDdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'IACQDDB'

    id = db.Column(db.Integer, primary_key=True)
    inc_id = db.Column(db.Integer)
    sale_id = db.Column(db.Integer)
    value = db.Column(db.Integer)
    payment = db.Column(db.Integer)

    def __init__(self, inc_id, sale_id, value, payment):
        self.inc_id = inc_id
        self.sale_id = sale_id
        self.value = value
        self.payment = payment
        
