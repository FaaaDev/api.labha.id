from main.shared.shared import db


class RetSaleHdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'RETSALEHDB'

    id = db.Column(db.Integer, primary_key=True)
    ret_code = db.Column(db.String(255), unique=True)
    ret_date = db.Column(db.TIMESTAMP)
    sale_id = db.Column(db.Integer)

    def __init__(self, ret_code, ret_date, sale_id):
        self.ret_code = ret_code
        self.ret_date = ret_date
        self.sale_id = sale_id
        