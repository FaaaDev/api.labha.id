from crypt import methods
from fileinput import filename
from pickle import TRUE
import re
from unittest import result
from flask import Flask, redirect, request, url_for, jsonify, make_response
from main.model.attendance import Attendance
from main.shared.shared import db, ma
from main.model.user import User
from main.schema.user import user_schema, users_schema
from main.schema.attendance import attendaces_schema, attendance_schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/HRISDATA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/upload')
app.config['SECRET_KEY'] = 'IKIKUNCIrahasiasu,rasahkeposia.pokonaulahHayangNYAhosiah.pateniraimu'
app.secret_key = 'IKIKUNCIrahasiasu,rasahkeposia.pokonaulahHayangNYAhosiah.pateniraimu'
CORS(app)


db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()


def target_url():
    return "https://itungin.id/"


def response(code, message, status, data):
    return jsonify({
        "code": code,
        "status": status,
        "message": message,
        "data": data
    }), code


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")
        # return 401 if token is not passed
        if not token:
            return response(401, "Token is missing !!", False, None)

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.query.filter(User.uid == data['id']).first()
        except Exception as e:
            return response(401, "Invalid or expired token !!", False, None)
        # returns the current logged in users contex to the routes
        return f(user, *args, **kwargs)

    return decorated


@app.route("/")
def index():
    return redirect(target_url())


@app.route("/v1/api/login", methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter(User.email == email).first()

    if user is None:
        return response(403, "Akun tidak ditemukan", False, None)
    else:
        if user.password != password:
            return response(403, "Password yang anda masukkan salah", False, None)
        else:
            token = jwt.encode({
                'id': user.uid,
                'exp': datetime.utcnow() + timedelta(hours=5)
            }, app.config['SECRET_KEY'])
            data = {
                "user": user_schema.dump(user),
                "token": token.decode('utf-8')
            }
            return response(200, "Berhasil", True, data)


@app.route("/v1/api/user", methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        try:
            username = request.json['username']
            phone = request.json['phone']
            email = request.json['email']
            password = request.json['password']
            image = ""
            dob = request.json['dob']

            user = User(username, password, phone, email, image, dob)
            db.session.add(user)
            db.session.commit()
            result = response(200, "Berhasil menambahkan user",
                              True, user_schema.dump(user))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Email sudah digunakan", False, None)
        finally:
            return result
    else:
        user = User.query.all()

        return response(200, "Berhasil", True, users_schema.dump(user))


@app.route('/v1/api/myprofile', methods=['GET'])
@token_required
def profil(self):
    user = User.query.filter(User.uid == self.uid).first()

    return response(200, "Berhasil", True, user_schema.dump(user))


@app.route('/v1/api/attendance', methods=['POST', 'GET'])
@token_required
def attendance(self):
    if request.method == 'POST':
        datein = datetime.utcnow().strftime("%d-%m-%y %X")
        locationin = request.json['location_in']

        att = Attendance(self.uid, datein, None, locationin, None, None, None)
        db.session.add(att)
        db.session.commit()

        return response(200, "Berhasil melakukan absensi masuk", True, attendance_schema.dump(att))
    else:
        att = Attendance.query.filter(Attendance.uid == self.uid).all()

        return response(200, "Berhasil", True, attendaces_schema.dump(att))

@app.route("/v1/api/attendance/<int:id>", methods=['PUT', 'GET', 'DELETE'])
@token_required
def attendance_id(self, id):
    att = Attendance.query.filter(Attendance.id == id).first()
    if request.method == 'PUT':
        locationout = request.json["location_out"]

        att.date_checkout = datetime.utcnow().strftime("%d-%m-%y %X")
        att.location_out = locationout
        db.session.commit()

        return response(200, "Berhasil melakukan absensi keluar", True, attendance_schema.dump(att))
    elif request.method == 'DELETE':
        if att.image_in != "" and att.image_in is not None:
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], att.image_in)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], att.image_in))
        if att.image_out != "" and att.image_out is not None:
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], att.image_out)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], att.image_out))

        db.session.delete(att)
        db.session.commit()

        return response(200, "Berhasil menghapus", True, None)
    else: 
        return response(200, "Berhasil", True, attendance_schema.dump(att))

@app.route('/v1/api/upload', methods=['POST'])
@token_required
def upload(self):
    file = request.files['image']
    file_name = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

    return response(200, "Berhasil mengupload gambar", True, file_name)

@app.route('/v1/api/upload/attendance/<int:id>', methods=['POST'])
@token_required
def upload_attendance(self, id):
    att = Attendance.query.filter(Attendance.id == id).first()
    if 'imagein' in request.files:
        file = request.files['imagein']
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        att.image_in = file_name
        db.session.commit()
        return response(200, "Berhasil mengupload gambar", True, file_name)
    elif 'imageout' in request.files:
        file = request.files['imageout']
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        att.image_out = file_name
        db.session.commit()
        return response(200, "Berhasil mengupload gambar", True, file_name)
    else:
        return response(400, "Tidak ada foto yang sesuai", True, None)