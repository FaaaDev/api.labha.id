from enum import unique
from main.shared.shared import db


class DjasaDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'DJASADDB'

    id = db.Column(db.Integer, primary_key=True)
    do_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    jasa_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    order = db.Column(db.Integer)
    price = db.Column(db.Float)
    disc = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, do_id, sup_id, jasa_id, unit_id, order, price, disc, total):
        self.do_id = do_id
        self.sup_id = sup_id
        self.jasa_id = jasa_id
        self.unit_id = unit_id
        self.order = order
        self.price = price
        self.disc = disc
        self.total = total
