from main.shared.shared import db


class AcqDdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'ACQDDB'

    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer)
    fk_id = db.Column(db.Integer)
    value = db.Column(db.Integer)
    payment = db.Column(db.Integer)
    dp = db.Column(db.Integer)

    def __init__(self, exp_id, fk_id, value, payment, dp):
        self.exp_id = exp_id
        self.fk_id = fk_id
        self.value = value
        self.payment = payment
        self.dp = dp
        
