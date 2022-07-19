from main.shared.shared import db

class HrgBlMdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'HRGBLMDB'

    id = db.Column(db.Integer, primary_key=True)
    ord_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    

    def __init__(self, ord_id, sup_id, prod_id, price):
        self.ord_id = ord_id
        self.sup_id = sup_id
        self.prod_id = prod_id
        self.price = price