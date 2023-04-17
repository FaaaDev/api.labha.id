from ..shared.shared import db

class AreaPenjualanMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'AREAMDB'

    id = db.Column(db.Integer, primary_key=True)
    area_pen_code = db.Column(db.String(255), unique=True)
    area_pen_name = db.Column(db.String(255))
    area_pen_ket = db.Column(db.Text)
    

    def __init__(self, area_pen_code, area_pen_name, area_pen_ket):
        self.area_pen_code = area_pen_code
        self.area_pen_name = area_pen_name
        self.area_pen_ket = area_pen_ket