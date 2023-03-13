from ..shared.shared import db


class SetupSAMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "SETUPSAMDB"

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    sto = db.Column(db.Integer)
    pur = db.Column(db.Integer)
    pur_shipping = db.Column(db.Integer)
    pur_retur = db.Column(db.Integer)
    pur_discount = db.Column(db.Integer)
    hpp = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        cp_id,
        sto,
        pur,
        pur_shipping,
        pur_retur,
        pur_discount,
        hpp,
        user_id
    ):
        self.cp_id = cp_id
        self.sto = sto
        self.pur = pur
        self.pur_shipping = pur_shipping
        self.pur_retur = pur_retur
        self.pur_discount = pur_discount
        self.hpp = hpp
        self.user_id = user_id
