from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db
import datetime


class GroupProMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "GPRODKMDB"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    div_code = db.Column(db.Integer)
    stok = db.Column(db.Boolean)
    wip = db.Column(db.Boolean)
    acc_sto = db.Column(db.Integer)
    acc_send = db.Column(db.Integer)
    acc_terima = db.Column(db.Integer)
    hrg_pokok = db.Column(db.Integer)
    acc_penj = db.Column(db.Integer)
    acc_wip = db.Column(db.Integer)
    potongan = db.Column(db.Integer)
    pengembalian = db.Column(db.Integer)
    selisih = db.Column(db.Integer)
    biaya = db.Column(db.Integer)

    def __init__(
        self,
        code,
        name,
        div_code,
        stok,
        wip,
        acc_sto,
        acc_send,
        acc_terima,
        hrg_pokok,
        acc_penj,
        acc_wip,
        potongan,
        pengembalian,
        selisih,
        biaya
    ):
        self.code = code
        self.name = name
        self.div_code = div_code
        self.stok = stok
        self.wip = wip
        self.acc_sto = acc_sto
        self.acc_send = acc_send
        self.acc_terima = acc_terima
        self.hrg_pokok = hrg_pokok
        self.acc_penj = acc_penj
        self.acc_wip = acc_wip
        self.potongan = potongan
        self.pengembalian = pengembalian
        self.selisih = selisih
        self.biaya = biaya
