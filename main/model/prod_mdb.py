from enum import unique
from ..shared.shared import db


class ProdMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "PRODMDB"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    group = db.Column(db.Integer)
    type = db.Column(db.Integer)
    codeb = db.Column(db.String(255))
    unit = db.Column(db.Integer)
    weight = db.Column(db.Float)
    dm_panjang = db.Column(db.Float)
    dm_lebar = db.Column(db.Float)
    dm_tinggi = db.Column(db.Float)
    suplier = db.Column(db.Integer)
    b_price = db.Column(db.Integer)
    s_price = db.Column(db.Integer)
    barcode = db.Column(db.String(255))
    metode = db.Column(db.Integer)
    max_stock = db.Column(db.Integer)
    min_stock = db.Column(db.Integer)
    re_stock = db.Column(db.Integer)
    lt_stock = db.Column(db.String(200))
    max_order = db.Column(db.Integer)
    image = db.Column(db.Text)
    ns = db.Column(db.Boolean)
    ket = db.Column(db.Text)
    imp = db.Column(db.Boolean)

    def __init__(
        self,
        code,
        name,
        group,
        type,
        codeb,
        unit,
        weight,
        dm_panjang,
        dm_lebar,
        dm_tinggi,
        suplier,
        b_price,
        s_price,
        barcode,
        metode,
        max_stock,
        min_stock,
        re_stock,
        lt_stock,
        max_order,
        image,
        ns,
        ket,
        imp
    ):
        self.code = code
        self.name = name
        self.group = group
        self.type = type
        self.codeb = codeb
        self.unit = unit
        self.weight = weight
        self.dm_panjang = dm_panjang
        self.dm_lebar = dm_lebar
        self.dm_tinggi = dm_tinggi
        self.suplier = suplier
        self.b_price = b_price
        self.s_price = s_price
        self.barcode = barcode
        self.metode = metode
        self.max_stock = max_stock
        self.min_stock = min_stock
        self.re_stock = re_stock
        self.lt_stock = lt_stock
        self.max_order = max_order
        self.image = image
        self.ns = ns
        self.ket = ket
        self.imp = imp
