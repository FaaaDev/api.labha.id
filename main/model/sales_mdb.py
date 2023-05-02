from enum import unique
from ..shared.shared import db

class SalesMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'SALESMDB'

    id = db.Column(db.Integer, primary_key=True)
    sales_code = db.Column(db.String(255), unique=True)
    sales_name = db.Column(db.String(255))
    sales_ket = db.Column(db.Text)
    

    def __init__(self, sales_code, sales_name, sales_ket):
        self.sales_code = sales_code
        self.sales_name = sales_name
        self.sales_ket = sales_ket