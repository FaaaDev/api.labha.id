from main.shared.shared import db

class AreaPenMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'AREAPENMDB'

    id = db.Column(db.Integer, primary_key=True)
    areaPen_code = db.Column(db.String(255), unique=True)
    areaPen_name = db.Column(db.String(255))
    areaPen_ket = db.Column(db.Text)
    

    def __init__(self, areaPen_code, areaPen_name, areaPen_ket):
        self.areaPen_code = areaPen_code
        self.areaPen_name = areaPen_name
        self.areaPen_ket = areaPen_ket