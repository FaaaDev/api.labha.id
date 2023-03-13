from main.shared.shared import db


class KorPiutangHdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'KPIUHDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(db.TIMESTAMP)
    cus_id = db.Column(db.Integer)
    type_kor = db.Column(db.String(5))
    value = db.Column(db.Integer)
    due_date = db.Column(db.TIMESTAMP)
    desc = db.Column(db.Text)
    user_id = db.Column(db.Integer)

    def __init__(self, code, date, cus_id, type_kor, value, due_date, desc, user_id):
        self.code = code
        self.date = date
        self.cus_id = cus_id
        self.type_kor = type_kor
        self.value = value
        self.due_date = due_date
        self.desc = desc
        self.user_id = user_id
