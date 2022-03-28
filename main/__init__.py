from crypt import methods
from fileinput import filename
from pickle import TRUE
import re
from sys import prefix
from unittest import result
from flask import Flask, redirect, request, url_for, jsonify, make_response
from main.model.bank_mdb import BankMdb
from main.shared.shared import db, ma
from main.model.user import User
from main.schema.user import user_schema, users_schema
from main.schema.bank_mdb import banks_schema, bank_schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/accdemo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = join(
    dirname(realpath(__file__)), 'static/upload')
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
            user = User.query.filter(User.id == data['id']).first()
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
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter(User.username == username).first()

    if user is None:
        return response(403, "Akun tidak ditemukan", False, None)
    else:
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            token = jwt.encode({
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=5)
            }, app.config['SECRET_KEY'])
            data = {
                "user": user_schema.dump(user),
                "token": token.decode('utf-8')
            }
            return response(200, "Berhasil", True, data)
        else:
            return response(403, "Password yang anda masukkan salah", False, None)


@app.route("/v1/api/user", methods=['POST', 'GET'])
@token_required
def user(self):
    if request.method == 'POST':
        try:
            username = request.json['username']
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']

            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            user = User(username, name, email,
                        hashed.decode(), None, None, None)
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


@app.route("/v1/api/user/<int:id>", methods=['PUT', 'GET', 'DELETE'])
@token_required
def user_id(self,id):
    user = User.query.filter(User.id == id).first()
    if request.method == 'PUT':
        username = request.json['username']
        user.username = username
        db.session.commit()

        return response(200, "Berhasil mengupdate user", True, user_schema.dump(user))
    elif request.method == 'DELETE':
        if user:
            db.session.delete(user)
            db.session.commit()
            return response(200, "Berhasil menghapus user", True, None)
        else:
            return response(200, "User tidak ditemukan", True, None)
    elif request.method == 'GET':
        return response(200, "Berhasil", True, user_schema.dump(user))
    else:
        return response(400, "Method not allowed!", True, user_schema.dump(user))


@app.route('/v1/api/myprofile', methods=['GET'])
@token_required
def profil(self):
    user = User.query.filter(User.id == self.id).first()

    return response(200, "Berhasil", True, user_schema.dump(user))

@app.route("/v1/api/bank-code", methods=['POST'])
@token_required
def bank_code(self):
    prefix = request.json['prefix']    

    if len(prefix) == 2:
        
        code = 1
        bc = prefix+"00"+str(code)
        bank = BankMdb.query.filter(BankMdb.BANK_CODE.like("%{}%".format(prefix))).order_by(BankMdb.BANK_CODE.desc()).all()
        if bank:
            code = int(bank[0].BANK_CODE.replace(prefix, ''))+1
            if code < 10:
                bc = prefix+"00"+str(code)
            else:
                if code > 99:
                    bc = prefix+str(code)
                else:
                    bc = prefix+"0"+str(code)

        print(bc)

        return response(200, "Berhasil", True, {"bank_code": bc.upper()})
    else:
        return ""

@app.route("/v1/api/bank", methods=['POST', 'GET'])
@token_required
def bank(self):
    if request.method == 'POST':
        return ''
    else:
        bank = BankMdb.query.all()
        return response(200, "Berhasil", True, banks_schema.dump(bank))


