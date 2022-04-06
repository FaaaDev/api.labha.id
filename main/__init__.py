from crypt import methods
from fileinput import filename
from pickle import TRUE
import re
from sys import prefix
from unittest import result
from flask import Flask, redirect, request, url_for, jsonify, make_response
from main.model.accou_mdb import AccouMdb
from main.model.adm_menu import AdmMenu
from main.model.adm_user_menu import AdmUserMenu
from main.model.bank_mdb import BankMdb
from main.model.klasi_mdb import KlasiMdb
from main.model.kateg_mdb import KategMdb
from main.shared.shared import db, ma
from main.model.user import User
from main.schema.user import user_schema, users_schema
from main.schema.bank_mdb import banks_schema, bank_schema
from main.schema.adm_user_menu import adm_user_menu_schema, adm_user_menus_schema, AdmUserMenuSchema
from main.schema.klasi_mdb import klasi_schema, klasies_schema, KlasiMdb as KlasiSchema
from main.schema.kateg_mdb import kateg_schema, kategs_schema, KategMdb as KategSchema
from main.schema.accou_mdb import accou_schema, accous_schema, AccouSchema
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/acc_dev'
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
def user_id(self, id):
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
    user = db.session.query(User, AdmUserMenu, AdmMenu)\
        .outerjoin(AdmUserMenu, AdmUserMenu.id_adm_user == User.id)\
        .outerjoin(AdmMenu, AdmMenu.id == AdmUserMenu.id_adm_menu)\
        .filter(User.id == self.id).all()

    menu = {
        "id": user[0][0].id,
        "email": user[0][0].email,
        "username": user[0][0].username,
        "name": user[0][0].name,
        "menu": [
            {
                "name": x[2].name,
                "sequence_no": x[2].sequence_no,
                "page_name": x[2].page_name,
                "route_name": x[2].route_name,
                "icon_file": x[2].icon_file,
                "akses": AdmUserMenuSchema(only=['view', 'edit', 'delete']).dump(x[1])
            }
            for x in user
        ]
    }

    return response(200, "Berhasil", True, menu)


@app.route("/v1/api/bank-code", methods=['POST'])
@token_required
def bank_code(self):
    prefix = request.json['prefix']

    if len(prefix) == 2:

        code = 1
        bc = prefix+"00"+str(code)
        bank = BankMdb.query.filter(BankMdb.BANK_CODE.like(
            "%{}%".format(prefix))).order_by(BankMdb.BANK_CODE.desc()).all()
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


@app.route("/v1/api/klasifikasi", methods=['POST', 'GET'])
@token_required
def klasifikasi(self):
    if request.method == 'POST':
        klasi = KlasiMdb(request.json['name'])
        db.session.add(klasi)
        db.session.commit()
        return response(200, "Berhasil", True, klasi_schema.dump(klasi))
    else:
        result = KlasiMdb.query.order_by(KlasiMdb.id.asc()).all()
        return response(200, "Berhasil", True, klasies_schema.dump(result))


@app.route("/v1/api/klasifikasi/<int:id>", methods=['PUT'])
@token_required
def klasifikasi_id(self, id):
    klasi = KlasiMdb.query.filter(KlasiMdb.id == id).first()
    klasi.klasiname = request.json['name']
    db.session.commit()

    return response(200, "Berhasil", True, klasi_schema.dump(klasi))


@app.route("/v1/api/kategory", methods=['POST', 'GET'])
@token_required
def kategory(self):
    if request.method == 'POST':
        name = request.json['name']
        kode_klasi = request.json['kode_klasi']
        kode_saldo = request.json['kode_saldo']
        kategory = KategMdb(name, kode_klasi, kode_saldo)
        db.session.add(kategory)
        db.session.commit()

        return response(200, "Berhasil", True, kateg_schema.dump(kategory))
    else:
        result = db.session.query(KategMdb, KlasiMdb)\
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)\
            .order_by(KategMdb.id.asc()).all()
        print(result)
        data = [
            {
                "kategory": kateg_schema.dump(x[0]),
                "klasifikasi": klasi_schema.dump(x[1])
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/kategory/<int:id>", methods=['PUT', 'GET', 'DELETE'])
@token_required
def kategory_id(self, id):
    kategory = KategMdb.query.filter(KategMdb.id == id).first()
    if request.method == 'PUT':
        kategory.name = request.json['name']
        kategory.kode_klasi = request.json['kode_klasi']
        kategory.kode_saldo = request.json['kode_saldo']
        db.session.commit()

        return response(200, "Berhasil", True, kateg_schema.dump(kategory))
    elif request.method == 'DELETE':
        db.session.delete(kategory)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = db.session.query(KategMdb, KlasiMdb)\
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)\
            .order_by(KategMdb.id.asc())\
            .filter(KategMdb.id == id).first()
        print(result)
        data = {
            "kategory": kateg_schema.dump(result[0]),
            "klasifikasi": klasi_schema.dump(result[1])
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/u/<int:kat_id>", methods=['GET'])
@token_required
def account_umum(self, kat_id):

    kategory = db.session.query(KategMdb, KlasiMdb)\
        .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)\
        .order_by(KategMdb.id.asc())\
        .filter(KategMdb.id == kat_id).first()

    key = str(kategory[1].id)+"."+str(kat_id)
    last_acc = AccouMdb.query.filter(and_(AccouMdb.acc_code.like("%{}%".format(
        key)), AccouMdb.dou_type == "U")).order_by(AccouMdb.acc_code.desc()).first()

    if last_acc != None:
        next_code = str(
            kategory[1].id)+"."+str(int(last_acc.acc_code.replace(str(kategory[1].id)+".", ""))+1)
    else:
        next_code = str(kategory[1].id)+"."+str(kat_id)+"0001"

    return response(200, "Berhasil", True, next_code)


@app.route("/v1/api/account/d/<string:umm_code>", methods=['GET'])
@token_required
def account_detail(self, umm_code):

    last_acc = AccouMdb.query.filter(AccouMdb.umm_code == umm_code).order_by(
        AccouMdb.acc_code.desc()).first()

    if last_acc != None:
        next_code = umm_code+"." + \
            str(int(last_acc.acc_code.replace(umm_code+".", ""))+1)
    else:
        next_code = umm_code+"."+"1"
    return response(200, "Berhasil", True, next_code)


@app.route("/v1/api/account", methods=['POST', 'GET'])
@token_required
def account(self):
    if request.method == 'POST':
        acc_code = request.json['kode_acc']
        acc_name = request.json['acc_name']
        umm_code = request.json['kode_umum']
        kat_code = request.json['kode_kategori']
        dou_type = request.json['du']
        sld_type = request.json['kode_saldo']
        connect = request.json['terhubung']
        sld_awal = request.json['saldo_awal']
        try:
            account = AccouMdb(acc_code, acc_name, umm_code,
                               kat_code, dou_type, sld_type, connect, sld_awal)
            db.session.add(account)
            db.session.commit()
            result = response(200, "Berhasil", True,
                              accou_schema.dump(account))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode akun "+acc_code+" sudah digunakan", False, None)
        finally:
            return result
    else:
        result = db.session.query(AccouMdb, KategMdb, KlasiMdb)\
            .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)\
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)\
            .order_by(AccouMdb.acc_code.asc()).all()
        print(result)
        data = [
            {
                "account": accou_schema.dump(x[0]),
                "kategory": kateg_schema.dump(x[1]),
                "klasifikasi": klasi_schema.dump(x[2])
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/umum", methods=['GET'])
@token_required
def acc_umum(self):
    result = db.session.query(AccouMdb, KategMdb, KlasiMdb)\
        .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)\
        .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)\
        .order_by(AccouMdb.acc_code.asc())\
        .filter(AccouMdb.dou_type == "U").all()
    print(result)
    data = [
        {
            "account": accou_schema.dump(x[0]),
            "kategory": kateg_schema.dump(x[1]),
            "klasifikasi": klasi_schema.dump(x[2])
        }
        for x in result
    ]

    return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/<int:id>", methods=['PUT', 'GET', 'DELETE'])
@token_required
def account_id(self, id):
    account = AccouMdb.query.filter(AccouMdb.id == id).first()
    if request.method == 'PUT':
        account.acc_code = request.json['kode_acc']
        account.acc_name = request.json['acc_name']
        account.umm_code = request.json['kode_umum']
        account.kat_code = request.json['kode_kategori']
        account.dou_type = request.json['du']
        account.sld_type = request.json['kode_saldo']
        account.connect = request.json['terhubung']
        account.sld_awal = request.json['saldo_awal']
        db.session.commit()

        return response(200, "Berhasil", True, accou_schema.dump(account))
    elif request.method == 'DELETE':
        db.session.delete(account)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = db.session.query(AccouMdb, KategMdb, KlasiMdb)\
            .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)\
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)\
            .order_by(AccouMdb.acc_code.asc())\
            .filter(AccouMdb.id == id).first()

        print(result)
        data = {
            "account": accou_schema.dump(result[0]),
            "kategory": kateg_schema.dump(result[1]),
            "klasifikasi": klasi_schema.dump(result[2])
        }

        return response(200, "Berhasil", True, data)
