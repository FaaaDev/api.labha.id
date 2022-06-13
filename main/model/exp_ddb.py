from main.shared.shared import db


class ExpDdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'EXPDDB'

    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer)
    acc_code = db.Column(db.Integer)
    value = db.Column(db.Integer)
    desc = db.Column(db.Text)

    def __init__(self, exp_id, acc_code, value, desc):
        self.exp_id = exp_id
        self.acc_code = acc_code
        self.value = value
        self.desc = desc
        
