from main.shared.shared import db


class GiroIncHdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'GRINCHDB'

    id = db.Column(db.Integer, primary_key=True)
    giro_date = db.Column(db.TIMESTAMP)
    giro_num = db.Column(db.String(255))
    bank_id = db.Column(db.Integer)
    pay_code = db.Column(db.Integer)
    pay_date = db.Column(db.TIMESTAMP)
    cus_id = db.Column(db.Integer)
    value = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, giro_date, giro_num, bank_id, pay_code, pay_date, cus_id, value, status):
        self.giro_date = giro_date
        self.bank_id = bank_id
        self.giro_num = giro_num
        self.pay_code = pay_code
        self.pay_date = pay_date
        self.cus_id = cus_id
        self.value = value
        self.status = status
        
