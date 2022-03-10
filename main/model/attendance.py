from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db

class Attendance(db.Model):
    __tablename__ = 'HR_ATT'

    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer)
    date_checkin = db.Column(db.String(200))
    image_in = db.Column(db.Text)
    location_in = db.Column(db.Text)
    date_checkout = db.Column(db.String(200))
    image_out = db.Column(db.Text)
    location_out = db.Column(db.Text)

    def __init__(self, uid, date_checkin, image_in, location_in, date_checkout, image_out, location_out):
        self.uid = uid
        self.date_checkin = date_checkin
        self.image_in = image_in
        self.location_in = location_in
        self.date_checkout = date_checkout
        self.image_out = image_out
        self.location_out = location_out