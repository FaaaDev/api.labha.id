import code
from crypt import methods
from fileinput import filename
from pickle import TRUE
import re
from sys import prefix
from unicodedata import name
from datetime import datetime
from flask import Flask, redirect, request, url_for, jsonify, make_response
import requests
from main.model.accou_mdb import AccouMdb
from main.model.adm_menu import AdmMenu
from main.model.adm_user_menu import AdmUserMenu
from main.model.bank_mdb import BankMdb
from main.model.ccost_mdb import CcostMdb
from main.model.comp_mdb import CompMdb
from main.model.jpel_mdb import JpelMdb
from main.model.jpem_mdb import JpemMdb
from main.model.sales_mdb import SalesMdb
from main.model.area_penjualan_mdb import AreaPenjualanMdb
from main.model.setup_mdb import SetupMdb
from main.model.sub_area_mdb import SubAreaMdb
from main.model.klasi_mdb import KlasiMdb
from main.model.kateg_mdb import KategMdb
from main.model.proj_mdb import ProjMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.syarat_bayar_mdb import RulesPayMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.custom_mdb import CustomerMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.divisi_mdb import DivisionMdb
from main.schema.ccost_mdb import ccost_schema, ccosts_schema, CcostSchema
from main.schema.proj_mdb import proj_schema, projs_schema, ProjSchema
from main.shared.shared import db, ma
from main.model.user import User
from main.schema.user import user_schema, users_schema
from main.schema.bank_mdb import banks_schema, bank_schema
from main.schema.adm_user_menu import (
    adm_user_menu_schema,
    adm_user_menus_schema,
    AdmUserMenuSchema,
)
from main.schema.klasi_mdb import klasi_schema, klasies_schema, KlasiMdb as KlasiSchema
from main.schema.kateg_mdb import kateg_schema, kategs_schema, KategMdb as KategSchema
from main.schema.accou_mdb import accou_schema, accous_schema, AccouSchema
from main.schema.jpel_mdb import jpels_schema, jpel_schema
from main.schema.jpem_mdb import jpems_schema, jpem_schema
from main.schema.sales_mdb import saless_schema, sales_schema
from main.schema.area_penjualan_mdb import area_penjualans_schema, area_penjualan_schema
from main.schema.sub_area_mdb import sub_areas_schema, sub_area_schema
from main.schema.currency_mdb import currencys_schema, currency_schema
from main.schema.syarat_bayar_mdb import rpays_schema, rpay_schema
from main.schema.lokasi_mdb import locts_schema, loct_schema
from main.schema.comp_mdb import comp_shcema, comps_schema, CompSchema
from main.schema.custom_mdb import customer_schema, customers_schema
from main.schema.supplier_mdb import supplier_schema, suppliers_schema
from main.schema.divisi_mdb import division_schema, divisions_schema
from main.schema.setup_mdb import *
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
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

server = SSHTunnelForwarder(
    ("103.179.56.92", 22),
    ssh_username="andynoer",
    ssh_password="Kulonuwun450",
    remote_bind_address=("127.0.0.1", 5432),
)

server.start()
local_port = str(server.local_bind_port)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:12345678@127.0.0.1:" + local_port + "/acc_dev"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["UPLOAD_FOLDER"] = join(dirname(realpath(__file__)), "static/upload")
app.config[
    "SECRET_KEY"
] = "IKIKUNCIrahasiasu,rasahkeposia.pokonaulahHayangNYAhosiah.pateniraimu"
app.secret_key = "IKIKUNCIrahasiasu,rasahkeposia.pokonaulahHayangNYAhosiah.pateniraimu"
CORS(app)


db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()


def target_url():
    return "https://itungin.id/"


def apiKey():
    return "42e8d306fd11942e83d509b631d52a48"


def cityUrl():
    return "https://api.rajaongkir.com/starter/city"


def response(code, message, status, data):
    return (
        jsonify({"code": code, "status": status, "message": message, "data": data}),
        code,
    )


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].replace("Bearer ", "")
        # return 401 if token is not passed
        if not token:
            return response(401, "Token is missing !!", False, None)

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
            user = User.query.filter(User.id == data["id"]).first()
        except Exception as e:
            return response(401, "Invalid or expired token !!", False, None)
        # returns the current logged in users contex to the routes
        return f(user, *args, **kwargs)

    return decorated


@app.route("/")
def index():
    return redirect(target_url())


@app.route("/v1/api/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    if "remember" in request.json:
        remember = request.json["remember"]
    else:
        remember = False

    print(remember)
    user = User.query.filter(User.username == username).first()

    if user is None:
        return response(403, "Akun tidak ditemukan", False, None)
    else:
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            if remember:
                token = jwt.encode(
                    {"id": user.id, "exp": datetime.utcnow() + timedelta(weeks=2)},
                    app.config["SECRET_KEY"],
                )
            else:
                token = jwt.encode(
                    {"id": user.id, "exp": datetime.utcnow() + timedelta(hours=5)},
                    app.config["SECRET_KEY"],
                )
            data = {"user": user_schema.dump(user), "token": token.decode("utf-8")}
            return response(200, "Berhasil", True, data)
        else:
            return response(403, "Password yang anda masukkan salah", False, None)


@app.route("/v1/api/user", methods=["POST", "GET"])
@token_required
def user(self):
    if request.method == "POST":
        try:
            username = request.json["username"]
            name = request.json["name"]
            email = request.json["email"]
            password = request.json["password"]

            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            user = User(username, name, email, hashed.decode(), None, None, None)
            db.session.add(user)
            db.session.commit()
            result = response(
                200, "Berhasil menambahkan user", True, user_schema.dump(user)
            )
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Email sudah digunakan", False, None)
        finally:
            return result
    else:
        user = User.query.all()
        return response(200, "Berhasil", True, users_schema.dump(user))


@app.route("/v1/api/user/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def user_id(self, id):
    user = User.query.filter(User.id == id).first()
    if request.method == "PUT":
        username = request.json["username"]
        user.username = username
        db.session.commit()

        return response(200, "Berhasil mengupdate user", True, user_schema.dump(user))
    elif request.method == "DELETE":
        if user:
            db.session.delete(user)
            db.session.commit()
            return response(200, "Berhasil menghapus user", True, None)
        else:
            return response(200, "User tidak ditemukan", True, None)
    elif request.method == "GET":
        return response(200, "Berhasil", True, user_schema.dump(user))
    else:
        return response(400, "Method not allowed!", True, user_schema.dump(user))


@app.route("/v1/api/myprofile", methods=["GET"])
@token_required
def profil(self):
    user = (
        db.session.query(User, AdmUserMenu, AdmMenu)
        .outerjoin(AdmUserMenu, AdmUserMenu.id_adm_user == User.id)
        .outerjoin(AdmMenu, AdmMenu.id == AdmUserMenu.id_adm_menu)
        .filter(User.id == self.id)
        .all()
    )

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
                "akses": AdmUserMenuSchema(only=["view", "edit", "delete"]).dump(x[1]),
            }
            for x in user
        ],
    }

    return response(200, "Berhasil", True, menu)


@app.route("/v1/api/bank", methods=["POST", "GET"])
@token_required
def bank(self):
    if request.method == "POST":
        try:
            BANK_CODE = request.json["BANK_CODE"]
            ACC_ID = request.json["ACC_ID"]
            BANK_NAME = request.json["BANK_NAME"]
            BANK_DESC = request.json["BANK_DESC"]
            bank = BankMdb(BANK_CODE, BANK_NAME, BANK_DESC, ACC_ID, self.id, None)
            db.session.add(bank)
            db.session.commit()

            result = response(200, "Berhasil", True, bank_schema.dump(bank))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            print(result)
            return result
    else:
        result = (
            db.session.query(BankMdb, AccouMdb)
            .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
            .order_by(BankMdb.id.asc())
            .all()
        )
        print(result)
        data = [
            {"bank": bank_schema.dump(x[0]), "account": accou_schema.dump(x[1])}
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/bank/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def bank_id(self, id):
    bank = BankMdb.query.filter(BankMdb.id == id).first()
    if request.method == "PUT":
        bank.BANK_CODE = request.json["BANK_CODE"]
        bank.acc_id = request.json["ACC_ID"]
        bank.BANK_NAMA = request.json["BANK_NAME"]
        bank.BANK_DESC = request.json["BANK_DESC"]
        db.session.commit()

        return response(200, "Berhasil", True, bank_schema.dump(bank))
    elif request.method == "DELETE":
        db.session.delete(bank)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(BankMdb, AccouMdb)
            .outerjoin(AccouMdb, BankMdb.BANK_ACC == AccouMdb.acc_code)
            .order_by(BankMdb.id.asc())
            .filter(BankMdb.id == id)
            .first()
        )
        print(result)
        data = {
            "bank": bank_schema.dump(result[0]),
            "account": accou_schema.dump(result[1]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/klasifikasi", methods=["POST", "GET"])
@token_required
def klasifikasi(self):
    if request.method == "POST":
        klasi = KlasiMdb(request.json["name"])
        db.session.add(klasi)
        db.session.commit()
        return response(200, "Berhasil", True, klasi_schema.dump(klasi))
    else:
        result = KlasiMdb.query.order_by(KlasiMdb.id.asc()).all()
        return response(200, "Berhasil", True, klasies_schema.dump(result))


@app.route("/v1/api/klasifikasi/<int:id>", methods=["PUT"])
@token_required
def klasifikasi_id(self, id):
    klasi = KlasiMdb.query.filter(KlasiMdb.id == id).first()
    klasi.klasiname = request.json["name"]
    db.session.commit()

    return response(200, "Berhasil", True, klasi_schema.dump(klasi))


@app.route("/v1/api/kategory", methods=["POST", "GET"])
@token_required
def kategory(self):
    if request.method == "POST":
        name = request.json["name"]
        kode_klasi = request.json["kode_klasi"]
        kode_saldo = request.json["kode_saldo"]
        kategory = KategMdb(name, kode_klasi, kode_saldo)
        db.session.add(kategory)
        db.session.commit()

        return response(200, "Berhasil", True, kateg_schema.dump(kategory))
    else:
        result = (
            db.session.query(KategMdb, KlasiMdb)
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
            .order_by(KategMdb.kode_klasi.asc())
            .order_by(KategMdb.id.asc())
            .all()
        )
        print(result)
        data = [
            {
                "kategory": kateg_schema.dump(x[0]),
                "klasifikasi": klasi_schema.dump(x[1]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/kategory/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def kategory_id(self, id):
    kategory = KategMdb.query.filter(KategMdb.id == id).first()
    if request.method == "PUT":
        kategory.name = request.json["name"]
        kategory.kode_klasi = request.json["kode_klasi"]
        kategory.kode_saldo = request.json["kode_saldo"]
        db.session.commit()

        return response(200, "Berhasil", True, kateg_schema.dump(kategory))
    elif request.method == "DELETE":
        db.session.delete(kategory)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(KategMdb, KlasiMdb)
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
            .order_by(KategMdb.id.asc())
            .filter(KategMdb.id == id)
            .first()
        )
        print(result)
        data = {
            "kategory": kateg_schema.dump(result[0]),
            "klasifikasi": klasi_schema.dump(result[1]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/u/<int:kat_id>", methods=["GET"])
@token_required
def account_umum(self, kat_id):

    kategory = (
        db.session.query(KategMdb, KlasiMdb)
        .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
        .order_by(KategMdb.id.asc())
        .filter(KategMdb.id == kat_id)
        .first()
    )

    key = str(kategory[1].id) + "." + str(kat_id)
    last_acc = (
        AccouMdb.query.filter(
            and_(AccouMdb.acc_code.like("%{}%".format(key)), AccouMdb.dou_type == "U")
        )
        .order_by(AccouMdb.acc_code.desc())
        .first()
    )

    if last_acc != None:
        next_code = (
            str(kategory[1].id)
            + "."
            + str(int(last_acc.acc_code.replace(str(kategory[1].id) + ".", "")) + 1)
        )
    else:
        next_code = str(kategory[1].id) + "." + str(kat_id) + "0001"

    return response(200, "Berhasil", True, next_code)


@app.route("/v1/api/account/d/<string:umm_code>", methods=["GET"])
@token_required
def account_detail(self, umm_code):

    last_acc = (
        AccouMdb.query.filter(AccouMdb.umm_code == umm_code)
        .order_by(AccouMdb.acc_code.desc())
        .first()
    )

    if last_acc != None:
        next_code = (
            umm_code + "." + str(int(last_acc.acc_code.replace(umm_code + ".", "")) + 1)
        )
    else:
        next_code = umm_code + "." + "1"
    return response(200, "Berhasil", True, next_code)


@app.route("/v1/api/account", methods=["POST", "GET"])
@token_required
def account(self):
    if request.method == "POST":
        acc_code = request.json["kode_acc"]
        acc_name = request.json["acc_name"]
        umm_code = request.json["kode_umum"]
        kat_code = request.json["kode_kategori"]
        dou_type = request.json["du"]
        sld_type = request.json["kode_saldo"]
        connect = request.json["terhubung"]
        sld_awal = request.json["saldo_awal"]
        try:
            account = AccouMdb(
                acc_code,
                acc_name,
                umm_code,
                kat_code,
                dou_type,
                sld_type,
                connect,
                sld_awal,
            )
            db.session.add(account)
            db.session.commit()
            result = response(200, "Berhasil", True, accou_schema.dump(account))
        except IntegrityError:
            db.session.rollback()
            result = response(
                400, "Kode akun " + acc_code + " sudah digunakan", False, None
            )
        finally:
            return result
    else:
        result = (
            db.session.query(AccouMdb, KategMdb, KlasiMdb)
            .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
            .order_by(KlasiMdb.id.asc())
            .order_by(KategMdb.id.asc())
            .order_by(AccouMdb.acc_code.asc())
            .all()
        )
        print(result)
        data = [
            {
                "account": accou_schema.dump(x[0]),
                "kategory": kateg_schema.dump(x[1]),
                "klasifikasi": klasi_schema.dump(x[2]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/umum", methods=["GET"])
@token_required
def acc_umum(self):
    result = (
        db.session.query(AccouMdb, KategMdb, KlasiMdb)
        .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)
        .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
        .order_by(AccouMdb.acc_code.asc())
        .filter(AccouMdb.dou_type == "U")
        .all()
    )
    print(result)
    data = [
        {
            "account": accou_schema.dump(x[0]),
            "kategory": kateg_schema.dump(x[1]),
            "klasifikasi": klasi_schema.dump(x[2]),
        }
        for x in result
    ]

    return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def account_id(self, id):
    account = AccouMdb.query.filter(AccouMdb.id == id).first()
    if request.method == "PUT":
        account.acc_code = request.json["kode_acc"]
        account.acc_name = request.json["acc_name"]
        account.umm_code = request.json["kode_umum"]
        account.kat_code = request.json["kode_kategori"]
        account.dou_type = request.json["du"]
        account.sld_type = request.json["kode_saldo"]
        account.connect = request.json["terhubung"]
        account.sld_awal = request.json["saldo_awal"]
        db.session.commit()

        return response(200, "Berhasil", True, accou_schema.dump(account))
    elif request.method == "DELETE":
        db.session.delete(account)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(AccouMdb, KategMdb, KlasiMdb)
            .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)
            .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
            .order_by(AccouMdb.acc_code.asc())
            .filter(AccouMdb.id == id)
            .first()
        )

        print(result)
        data = {
            "account": accou_schema.dump(result[0]),
            "kategory": kateg_schema.dump(result[1]),
            "klasifikasi": klasi_schema.dump(result[2]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/cost-center", methods=["POST", "GET"])
@token_required
def ccost(self):
    if request.method == "POST":
        try:
            code = request.json["ccost_code"]
            name = request.json["ccost_name"]
            keterangan = request.json["ccost_ket"]
            cost = CcostMdb(code, name, keterangan)
            db.session.add(cost)
            db.session.commit()
            result = response(200, "Berhasil", True, ccost_schema.dump(cost))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = CcostMdb.query.all()

        return response(200, "Berhasil", True, ccosts_schema.dump(result))


@app.route("/v1/api/cost-center/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def ccost_id(self, id):
    cost = CcostMdb.query.filter(CcostMdb.id == id).first()
    if request.method == "PUT":
        try:
            cost.ccost_code = request.json["ccost_code"]
            cost.ccost_name = request.json["ccost_name"]
            cost.ccost_ket = request.json["ccost_ket"]
            db.session.commit()

            result = response(200, "Berhasil", True, ccost_schema.dump(cost))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(cost)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, ccost_schema.dump(cost))


@app.route("/v1/api/project", methods=["POST", "GET"])
@token_required
def proj(self):
    if request.method == "POST":
        try:
            code = request.json["proj_code"]
            name = request.json["proj_name"]
            keterangan = request.json["proj_ket"]
            project = ProjMdb(code, name, keterangan)
            db.session.add(project)
            db.session.commit()

            result = response(200, "Berhasil", True, proj_schema.dump(project))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = ProjMdb.query.all()

        return response(200, "Berhasil", True, projs_schema.dump(result))


@app.route("/v1/api/project/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def proj_id(self, id):
    project = ProjMdb.query.filter(ProjMdb.id == id).first()
    if request.method == "PUT":
        try:
            project.proj_code = request.json["proj_code"]
            project.proj_name = request.json["proj_name"]
            project.proj_ket = request.json["proj_ket"]
            db.session.commit()
            result = response(200, "Berhasil", True, proj_schema.dump(project))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(project)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, proj_schema.dump(project))


# Jenis Pelanggan
@app.route("/v1/api/jenis-pelanggan", methods=["POST", "GET"])
@token_required
def jpel(self):
    if request.method == "POST":
        try:
            jpel_code = request.json["jpel_code"]
            jpel_name = request.json["jpel_name"]
            jpel_ket = request.json["jpel_ket"]
            jenis_pel = JpelMdb(jpel_code, jpel_name, jpel_ket)
            db.session.add(jenis_pel)
            db.session.commit()

            result = response(200, "Berhasil", True, jpel_schema.dump(jenis_pel))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = JpelMdb.query.all()

        return response(200, "Berhasil", True, jpels_schema.dump(result))


@app.route("/v1/api/jenis-pelanggan/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def jpel_id(self, id):
    jenis_pel = JpelMdb.query.filter(JpelMdb.id == id).first()
    if request.method == "PUT":
        try:
            jenis_pel.jpel_code = request.json["jpel_code"]
            jenis_pel.jpel_name = request.json["jpel_name"]
            jenis_pel.jpel_ket = request.json["jpel_ket"]
            db.session.commit()
            result = response(200, "Berhasil", True, jpel_schema.dump(jenis_pel))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(jenis_pel)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, jpel_schema.dump(jenis_pel))


# Jenis Pemasok
@app.route("/v1/api/jenis-pemasok", methods=["POST", "GET"])
@token_required
def jpem(self):
    if request.method == "POST":
        try:
            jpem_code = request.json["jpem_code"]
            jpem_name = request.json["jpem_name"]
            jpem_ket = request.json["jpem_ket"]
            jenisPem = JpemMdb(jpem_code, jpem_name, jpem_ket)
            db.session.add(jenisPem)
            db.session.commit()

            result = response(200, "Berhasil", True, jpem_schema.dump(jenisPem))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = JpemMdb.query.all()

        return response(200, "Berhasil", True, jpems_schema.dump(result))


@app.route("/v1/api/jenis-pemasok/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def jpem_id(self, id):
    jenis_pem = JpemMdb.query.filter(JpemMdb.id == id).first()
    if request.method == "PUT":
        try:
            jenis_pem.jpem_code = request.json["jpem_code"]
            jenis_pem.jpem_name = request.json["jpem_name"]
            jenis_pem.jpem_ket = request.json["jpem_ket"]
            db.session.commit()
            result = response(200, "Berhasil", True, jpem_schema.dump(jenis_pem))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(jenis_pem)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, jpem_schema.dump(jenis_pem))


# Salesman
@app.route("/v1/api/salesman", methods=["POST", "GET"])
@token_required
def sales(self):
    if request.method == "POST":
        try:
            sales_code = request.json["sales_code"]
            sales_name = request.json["sales_name"]
            sales_ket = request.json["sales_ket"]
            salesman = SalesMdb(sales_code, sales_name, sales_ket)
            db.session.add(salesman)
            db.session.commit()

            result = response(200, "Berhasil", True, sales_schema.dump(salesman))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = SalesMdb.query.all()

        return response(200, "Berhasil", True, saless_schema.dump(result))


@app.route("/v1/api/salesman/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def sales_id(self, id):
    salesman = SalesMdb.query.filter(SalesMdb.id == id).first()
    if request.method == "PUT":
        try:
            salesman.sales_code = request.json["sales_code"]
            salesman.sales_name = request.json["sales_name"]
            salesman.sales_ket = request.json["sales_ket"]
            db.session.commit()
            result = response(200, "Berhasil", True, sales_schema.dump(salesman))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(salesman)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, sales_schema.dump(salesman))


# Area Penjualan
@app.route("/v1/api/area-penjualan", methods=["POST", "GET"])
@token_required
def area_pen(self):
    if request.method == "POST":
        try:
            area_pen_code = request.json["area_pen_code"]
            area_pen_name = request.json["area_pen_name"]
            area_pen_ket = request.json["area_pen_ket"]
            area_pen = AreaPenjualanMdb(area_pen_code, area_pen_name, area_pen_ket)
            db.session.add(area_pen)
            db.session.commit()

            result = response(
                200, "Berhasil", True, area_penjualan_schema.dump(area_pen)
            )
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = AreaPenjualanMdb.query.all()

        return response(200, "Berhasil", True, area_penjualans_schema.dump(result))


@app.route("/v1/api/area-penjualan/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def area_pen_id(self, id):
    area_pen = AreaPenjualanMdb.query.filter(AreaPenjualanMdb.id == id).first()
    if request.method == "PUT":
        try:
            area_pen.area_pen_code = request.json["area_pen_code"]
            area_pen.area_pen_name = request.json["area_pen_name"]
            area_pen.area_pen_ket = request.json["area_pen_ket"]
            db.session.commit()
            result = response(
                200, "Berhasil", True, area_penjualan_schema.dump(area_pen)
            )
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(area_pen)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, area_penjualan_schema.dump(area_pen))


# Sub Area Penjualan
@app.route("/v1/api/sub-area", methods=["POST", "GET"])
@token_required
def subArea(self):
    if request.method == "POST":
        sub_code = request.json["sub_code"]
        sub_area_code = request.json["sub_area_code"]
        sub_name = request.json["sub_name"]
        sub_ket = request.json["sub_ket"]
        subArea = SubAreaMdb(sub_code, sub_area_code, sub_name, sub_ket)
        db.session.add(subArea)
        db.session.commit()

        return response(200, "Berhasil", True, sub_area_schema.dump(subArea))
    else:
        result = (
            db.session.query(SubAreaMdb, AreaPenjualanMdb)
            .outerjoin(
                AreaPenjualanMdb, SubAreaMdb.sub_area_code == AreaPenjualanMdb.id
            )
            .order_by(SubAreaMdb.id.asc())
            .all()
        )
        print(result)
        data = [
            {
                "subArea": sub_area_schema.dump(x[0]),
                "areaPen": area_penjualan_schema.dump(x[1]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/sub-area/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def sub_area_id(self, id):
    subArea = SubAreaMdb.query.filter(SubAreaMdb.id == id).first()
    if request.method == "PUT":
        subArea.sub_code = request.json["sub_code"]
        subArea.sub_area_code = request.json["sub_area_code"]
        subArea.sub_name = request.json["sub_name"]
        subArea.sub_ket = request.json["sub_ket"]
        db.session.commit()

        return response(200, "Berhasil", True, sub_area_schema.dump(subArea))
    elif request.method == "DELETE":
        db.session.delete(subArea)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(SubAreaMdb, AreaPenjualanMdb)
            .outerjoin(
                AreaPenjualanMdb, SubAreaMdb.sub_area_code == AreaPenjualanMdb.id
            )
            .order_by(SubAreaMdb.id.asc())
            .all()
        )
        print(result)
        data = {
            "subArea": sub_area_schema.dump([0]),
            "areaPen": area_penjualan_schema.dump([1]),
        }

        return response(200, "Berhasil", True, data)


# Currency
@app.route("/v1/api/currency", methods=["POST", "GET"])
@token_required
def currency(self):
    if request.method == "POST":
        try:
            code = request.json["code"]
            name = request.json["name"]
            date = request.json["date"]
            rate = request.json["rate"]
            curren = CurrencyMdb(code, name, date, rate)
            db.session.add(curren)
            db.session.commit()

            result = response(200, "Berhasil", True, currency_schema.dump(curren))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = CurrencyMdb.query.all()

        return response(200, "Berhasil", True, currencys_schema.dump(result))


@app.route("/v1/api/currency/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def currency_id(self, id):
    curren = CurrencyMdb.query.filter(CurrencyMdb.id == id).first()
    if request.method == "PUT":
        try:
            curren.code = request.json["code"]
            curren.name = request.json["name"]
            curren.date = request.json["date"]
            curren.rate = request.json["rate"]
            db.session.commit()
            result = response(200, "Berhasil", True, currency_schema.dump(curren))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(curren)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, currency_schema.dump(curren))


# Rules Payment
@app.route("/v1/api/rules-payment", methods=["POST", "GET"])
@token_required
def rules_pay(self):
    if request.method == "POST":
        try:
            name = request.json["name"]
            day = request.json["day"]
            ket = request.json["ket"]
            rules_pay = RulesPayMdb(name, day, ket)
            db.session.add(rules_pay)
            db.session.commit()

            result = response(200, "Berhasil", True, rpay_schema.dump(rules_pay))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = RulesPayMdb.query.all()

        return response(200, "Berhasil", True, rpays_schema.dump(result))


@app.route("/v1/api/rules-payment/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def rules_pay_id(self, id):
    rules_pay = RulesPayMdb.query.filter(RulesPayMdb.id == id).first()
    if request.method == "PUT":
        try:
            rules_pay.name = request.json["name"]
            rules_pay.day = request.json["day"]
            rules_pay.ket = request.json["ket"]
            db.session.commit()
            result = response(200, "Berhasil", True, rpay_schema.dump(rules_pay))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(rules_pay)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, rpay_schema.dump(rules_pay))


# Lokasi
@app.route("/v1/api/lokasi", methods=["POST", "GET"])
@token_required
def lokasi(self):
    if request.method == "POST":
        try:
            code = request.json["code"]
            name = request.json["name"]
            address = request.json["address"]
            desc = request.json["desc"]
            lokasi = LocationMdb(code, name, address, desc)
            db.session.add(lokasi)
            db.session.commit()

            result = response(200, "Berhasil", True, loct_schema.dump(lokasi))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = LocationMdb.query.all()

        return response(200, "Berhasil", True, locts_schema.dump(result))


@app.route("/v1/api/lokasi/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def lokasi_id(self, id):
    lokasi = LocationMdb.query.filter(LocationMdb.id == id).first()
    if request.method == "PUT":
        try:
            lokasi.code = request.json["code"]
            lokasi.name = request.json["name"]
            lokasi.address = request.json["address"]
            lokasi.desc = request.json["desc"]
            db.session.commit()
            result = response(200, "Berhasil", True, loct_schema.dump(lokasi))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(lokasi)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, loct_schema.dump(lokasi))


@app.route("/v1/api/upload", methods=["POST"])
@token_required
def upload(self):
    file = request.files["image"]
    file_name = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

    return response(200, "Berhasil mengupload gambar", True, file_name)


@app.route("/v1/api/company", methods=["POST", "GET"])
@token_required
def company(self):
    if request.method == "POST":
        try:
            cp_name = request.json["cp_name"]
            cp_addr = request.json["cp_addr"]
            cp_ship_addr = request.json["cp_ship_addr"]
            cp_telp = request.json["cp_telp"]
            cp_email = request.json["cp_email"]
            cp_webs = request.json["cp_webs"]
            cp_npwp = request.json["cp_npwp"]
            cp_coper = request.json["cp_coper"]
            cp_logo = request.json["cp_logo"]
            multi_currency = request.json["multi_currency"]
            appr_po = request.json["appr_po"]
            appr_payment = request.json["appr_payment"]
            over_stock = request.json["over_stock"]
            discount = request.json["discount"]
            tiered = request.json["tiered"]
            rp = request.json["rp"]
            over_po = request.json["over_po"]

            company = CompMdb(
                cp_name,
                cp_addr,
                cp_ship_addr,
                cp_telp,
                cp_email,
                cp_webs,
                cp_npwp,
                cp_coper,
                cp_logo,
                multi_currency,
                appr_po,
                appr_payment,
                over_stock,
                discount,
                tiered,
                rp,
                over_po,
            )
            db.session.add(company)
            db.session.commit()

            user = User.query.filter(User.id == self.id).first()
            user.company = company.id
            db.session.commit()

            result = response(200, "Berhasil", True, comp_shcema.dump(company))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = (
            db.session.query(User, CompMdb)
            .outerjoin(CompMdb, User.company == CompMdb.id)
            .filter(User.id == self.id)
            .first()
        )

        if result[1]:
            result[1].cp_logo = (
                request.host_url + "static/upload/" + result[1].cp_logo
                if result[1].cp_logo != ""
                else ""
            )

        return response(200, "Berhasil", True, comp_shcema.dump(result[1]))


@app.route("/v1/api/company/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def company_id(self, id):
    company = CompMdb.query.filter(CompMdb.id == id).first()
    if request.method == "PUT":
        try:
            company.cp_name = request.json["cp_name"]
            company.cp_addr = request.json["cp_addr"]
            company.cp_ship_addr = request.json["cp_ship_addr"]
            company.cp_telp = request.json["cp_telp"]
            company.cp_email = request.json["cp_email"]
            company.cp_webs = request.json["cp_webs"]
            company.cp_npwp = request.json["cp_npwp"]
            company.cp_coper = request.json["cp_coper"]

            if request.host_url + "static/upload/" in request.json["cp_logo"]:
                cp_logo = request.json["cp_logo"].replace(
                    request.host_url + "static/upload/", ""
                )
            else:
                cp_logo = request.json["cp_logo"]

            if company.cp_logo != cp_logo:
                if company.cp_logo != "" and company.cp_logo is not None:
                    if os.path.exists(
                        os.path.join(app.config["UPLOAD_FOLDER"], company.cp_logo)
                    ):
                        os.remove(
                            os.path.join(app.config["UPLOAD_FOLDER"], company.cp_logo)
                        )

            company.cp_logo = cp_logo
            company.multi_currency = request.json["multi_currency"]
            company.appr_po = request.json["appr_po"]
            company.appr_payment = request.json["appr_payment"]
            company.over_stock = request.json["over_stock"]
            company.discount = request.json["discount"]
            company.tiered = request.json["tiered"]
            company.rp = request.json["rp"]
            company.over_po = request.json["over_po"]

            db.session.commit()

            result = response(200, "Berhasil", True, comp_shcema.dump(company))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(company)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, comp_shcema.dump(company))


@app.route("/v1/api/customer", methods=["POST", "GET"])
@token_required
def customer(self):
    if request.method == "POST":
        cus_code = request.json["cus_code"]
        cus_name = request.json["cus_name"]
        cus_jpel = request.json["cus_jpel"]
        cus_sub_area = request.json["cus_sub_area"]
        cus_npwp = request.json["cus_npwp"]
        cus_address = request.json["cus_address"]
        cus_kota = request.json["cus_kota"]
        cus_kpos = request.json["cus_kpos"]
        cus_telp1 = request.json["cus_telp1"]
        cus_telp2 = request.json["cus_telp2"]
        cus_email = request.json["cus_email"]
        cus_fax = request.json["cus_fax"]
        cus_cp = request.json["cus_cp"]
        cus_curren = request.json["cus_curren"]
        cus_pjk = request.json["cus_pjk"]
        cus_ket = request.json["cus_ket"]
        cus_gl = request.json["cus_gl"]
        cus_uang_muka = request.json["cus_uang_muka"]
        cus_limit = request.json["cus_limit"]
        try:
            customer = CustomerMdb(
                cus_code,
                cus_name,
                cus_jpel,
                cus_sub_area,
                cus_npwp,
                cus_address,
                cus_kota,
                cus_kpos,
                cus_telp1,
                cus_telp2,
                cus_email,
                cus_fax,
                cus_cp,
                cus_curren,
                cus_pjk,
                cus_ket,
                cus_gl,
                cus_uang_muka,
                cus_limit,
            )
            db.session.add(customer)
            db.session.commit()
            result = response(200, "Berhasil", True, customer_schema.dump(customer))
        except IntegrityError:
            db.session.rollback()
            result = response(
                400, "Kode akun " + cus_code + " sudah digunakan", False, None
            )
        finally:
            return result
    else:
        result = (
            db.session.query(CustomerMdb, JpelMdb, SubAreaMdb, CurrencyMdb)
            .outerjoin(JpelMdb, JpelMdb.id == CustomerMdb.cus_jpel)
            .outerjoin(SubAreaMdb, SubAreaMdb.id == CustomerMdb.cus_sub_area)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == CustomerMdb.cus_curren)
            .order_by(JpelMdb.id.asc())
            .order_by(CurrencyMdb.id.asc())
            .order_by(CustomerMdb.cus_code.asc())
            .all()
        )
        print(result)
        data = [
            {
                "customer": customer_schema.dump(x[0]),
                "jpel": jpel_schema.dump(x[1]),
                "subArea": sub_area_schema.dump(x[2]),
                "currency": currency_schema.dump(x[3]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/customer/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def customer_id(self, id):
    customer = CustomerMdb.query.filter(CustomerMdb.id == id).first()
    if request.method == "PUT":
        customer.cus_code = request.json["cus_code"]
        customer.cus_name = request.json["cus_name"]
        customer.cus_jpel = request.json["cus_jpel"]
        customer.cus_sub_area = request.json["cus_sub_area"]
        customer.cus_npwp = request.json["cus_npwp"]
        customer.cus_address = request.json["cus_address"]
        customer.cus_kota = request.json["cus_kota"]
        customer.cus_kpos = request.json["cus_kpos"]
        customer.cus_telp1 = request.json["cus_telp1"]
        customer.cus_telp2 = request.json["cus_telp2"]
        customer.cus_email = request.json["cus_email"]
        customer.cus_fax = request.json["cus_fax"]
        customer.cus_cp = request.json["cus_cp"]
        customer.cus_curren = request.json["cus_curren"]
        customer.cus_pjk = request.json["cus_pjk"]
        customer.cus_ket = request.json["cus_ket"]
        customer.cus_gl = request.json["cus_gl"]
        customer.cus_uang_muka = request.json["cus_uang_muka"]
        customer.cus_limit = request.json["cus_limit"]
        db.session.commit()

        return response(200, "Berhasil", True, customer_schema.dump(customer))
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(CustomerMdb, JpelMdb, SubAreaMdb, CurrencyMdb)
            .outerjoin(JpelMdb, JpelMdb.id == CustomerMdb.cus_jpel)
            .outerjoin(SubAreaMdb, SubAreaMdb.id == CustomerMdb.cus_sub_area)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == CustomerMdb.cus_curren)
            .order_by(CustomerMdb.cus_code.asc())
            .filter(CustomerMdb.id == id)
            .first()
        )

        print(result)
        data = {
            "customer": customer_schema.dump(result[0]),
            "jpel": jpel_schema.dump(result[1]),
            "subArea": sub_area_schema.dump(result[2]),
            "currency": currency_schema.dump(result[3]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/supplier", methods=["POST", "GET"])
@token_required
def supplier(self):
    if request.method == "POST":
        sup_code = request.json["sup_code"]
        sup_name = request.json["sup_name"]
        sup_jpem = request.json["sup_jpem"]
        sup_ppn = request.json["sup_ppn"]
        sup_npwp = request.json["sup_npwp"]
        sup_address = request.json["sup_address"]
        sup_kota = request.json["sup_kota"]
        sup_kpos = request.json["sup_kpos"]
        sup_telp1 = request.json["sup_telp1"]
        sup_telp2 = request.json["sup_telp2"]
        sup_fax = request.json["sup_fax"]
        sup_cp = request.json["sup_cp"]
        sup_curren = request.json["sup_curren"]
        sup_ket = request.json["sup_ket"]
        sup_hutang = request.json["sup_hutang"]
        sup_uang_muka = request.json["sup_uang_muka"]
        sup_limit = request.json["sup_limit"]
        try:
            supplier = SupplierMdb(
                sup_code,
                sup_name,
                sup_jpem,
                sup_ppn,
                sup_npwp,
                sup_address,
                sup_kota,
                sup_kpos,
                sup_telp1,
                sup_telp2,
                sup_fax,
                sup_cp,
                sup_curren,
                sup_ket,
                sup_hutang,
                sup_uang_muka,
                sup_limit,
            )
            db.session.add(supplier)
            db.session.commit()
            result = response(200, "Berhasil", True, supplier_schema.dump(supplier))
        except IntegrityError:
            db.session.rollback()
            result = response(
                400, "Kode akun " + sup_code + " sudah digunakan", False, None
            )
        finally:
            return result
    else:
        result = (
            db.session.query(SupplierMdb, JpemMdb, CurrencyMdb)
            .outerjoin(JpemMdb, JpemMdb.id == SupplierMdb.sup_jpem)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == SupplierMdb.sup_curren)
            .order_by(JpemMdb.id.asc())
            .order_by(CurrencyMdb.id.asc())
            .order_by(SupplierMdb.sup_code.asc())
            .all()
        )
        print(result)
        data = [
            {
                "supplier": supplier_schema.dump(x[0]),
                "jpem": jpem_schema.dump(x[1]),
                "currency": currency_schema.dump(x[2]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/supplier/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def supplier_id(self, id):
    supplier = SupplierMdb.query.filter(SupplierMdb.id == id).first()
    if request.method == "PUT":
        supplier.sup_code = request.json["sup_code"]
        supplier.sup_name = request.json["sup_name"]
        supplier.sup_jpem = request.json["sup_jpem"]
        supplier.sup_ppn = request.json["sup_ppn"]
        supplier.sup_npwp = request.json["sup_npwp"]
        supplier.sup_address = request.json["sup_address"]
        supplier.sup_kota = request.json["sup_kota"]
        supplier.sup_kpos = request.json["sup_kpos"]
        supplier.sup_telp1 = request.json["sup_telp1"]
        supplier.sup_telp2 = request.json["sup_telp2"]
        supplier.sup_fax = request.json["sup_fax"]
        supplier.sup_cp = request.json["sup_cp"]
        supplier.sup_curren = request.json["sup_curren"]
        supplier.sup_ket = request.json["sup_ket"]
        supplier.sup_hutang = request.json["sup_hutang"]
        supplier.sup_uang_muka = request.json["sup_uang_muka"]
        supplier.sup_limit = request.json["sup_limit"]
        db.session.commit()

        return response(200, "Berhasil", True, supplier_schema.dump(supplier))
    elif request.method == "DELETE":
        db.session.delete(supplier)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(SupplierMdb, JpelMdb, CurrencyMdb)
            .join(JpemMdb, JpelMdb.id == SupplierMdb.sup_jpem)
            .join(CurrencyMdb, CurrencyMdb.id == SupplierMdb.sup_curren)
            .order_by(SupplierMdb.sup_code.asc())
            .filter(SupplierMdb.id == id)
            .first()
        )

        print(result)
        data = {
            "supplier": supplier_schema.dump(result[0]),
            "jpem": jpem_schema.dump(result[1]),
            "currency": currency_schema.dump(result[2]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/city")
@token_required
def city(self):
    api_url = cityUrl()
    header = {"key": apiKey()}
    result = requests.get(url=api_url, headers=header).json()

    if result["rajaongkir"]["status"]["code"] == 200:
        return response(200, "Berhasil", True, result["rajaongkir"]["results"])
    else:
        return response(200, "Berhasil", True, None)


@app.route("/v1/api/setup/account", methods=["POST", "GET"])
@token_required
def setup_account(self):
    user = User.query.filter(User.id == self.id).first()
    if request.method == "POST":
        try:
            cp_id = user.company
            ar = request.json["ar"]
            ap = request.json["ap"]
            pnl = request.json["pnl"]
            pnl_year = request.json["pnl_year"]
            rtn_income = request.json["rtn_income"]
            sls_rev = request.json["sls_rev"]
            sls_disc = request.json["sls_disc"]
            sls_retur = request.json["sls_retur"]
            sls_shipping = request.json["sls_shipping"]
            sls_prepaid = request.json["sls_prepaid"]
            sls_unbill = request.json["sls_unbill"]
            sls_unbill_recv = request.json["sls_unbill_recv"]
            sls_tax = request.json["sls_tax"]
            pur_cogs = request.json["pur_cogs"]
            pur_discount = request.json["pur_discount"]
            pur_shipping = request.json["pur_shipping"]
            pur_retur = request.json["pur_retur"]
            pur_advance = request.json["pur_advance"]
            pur_unbill = request.json["pur_unbill"]
            pur_tax = request.json["pur_tax"]
            sto = request.json["sto"]
            sto_broken = request.json["sto_broken"]
            sto_hpp_diff = request.json["sto_hpp_diff"]
            sto_general =request.json["sto_general"]
            sto_production=request.json["sto_production"]
            fixed_assets = request.json["fixed_assets"]

            setup = SetupMdb(
                cp_id,
                ar,
                ap,
                pnl,
                pnl_year,
                rtn_income,
                sls_rev,
                sls_disc,
                sls_retur,
                sls_shipping,
                sls_prepaid,
                sls_unbill,
                sls_unbill_recv,
                sls_tax,
                pur_cogs,
                pur_discount,
                pur_shipping,
                pur_retur,
                pur_advance,
                pur_unbill,
                pur_tax,
                sto,
                sto_broken,
                sto_general,
                sto_production,
                sto_hpp_diff,
                fixed_assets,
            )
            db.session.add(setup)
            db.session.commit()

            result = response(200, "Berhasil", True, setup_shcema.dump(setup))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        setup = SetupMdb.query.filter(SetupMdb.cp_id == user.company).first()
        account = AccouMdb.query.all()

        if(setup):
            setup_dict = dict((col, getattr(setup, col)) for col in setup.__table__.columns.keys())

            for key, value in setup_dict.items():
                if key != 'id' and key != "cp_id":
                    for x in account:
                        if value:
                            if value == x.id:
                                setup_dict[key] = accou_schema.dump(x)
            
            return response(200, "Berhasil", True, setup_dict)
            
        return response(200, "Berhasil", False, None)
        
@app.route("/v1/api/setup/account/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def setup_account_id(self, id):
    setup = SetupMdb.query.filter(SetupMdb.id == id).first()
    if request.method == "PUT":
        setup.ar = request.json["ar"]
        setup.ap = request.json["ap"]
        setup.pnl = request.json["pnl"]
        setup.pnl_year = request.json["pnl_year"]
        setup.rtn_income = request.json["rtn_income"]
        setup.sls_rev = request.json["sls_rev"]
        setup.sls_disc = request.json["sls_disc"]
        setup.sls_retur = request.json["sls_retur"]
        setup.sls_shipping = request.json["sls_shipping"]
        setup.sls_prepaid = request.json["sls_prepaid"]
        setup.sls_unbill = request.json["sls_unbill"]
        setup.sls_unbill_recv = request.json["sls_unbill_recv"]
        setup.sls_tax = request.json["sls_tax"]
        setup.pur_cogs = request.json["pur_cogs"]
        setup.pur_discount = request.json["pur_discount"]
        setup.pur_shipping = request.json["pur_shipping"]
        setup.pur_retur = request.json["pur_retur"]
        setup.pur_advance = request.json["pur_advance"]
        setup.pur_unbill = request.json["pur_unbill"]
        setup.pur_tax = request.json["pur_tax"]
        setup.sto = request.json["sto"]
        setup.sto_broken = request.json["sto_broken"]
        setup.sto_general =request.json["sto_general"]
        setup.sto_production=request.json["sto_production"]
        setup.sto_hpp_diff = request.json["sto_hpp_diff"]
        setup.fixed_assets = request.json["fixed_assets"]
        db.session.commit()

        return response(200, "Berhasil", True, setup_shcema.dump(setup))
    elif request.method == "DELETE":
        db.session.delete(setup)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        account = AccouMdb.query.all()

        if setup:
            setup_dict = dict((col, getattr(setup, col)) for col in setup.__table__.columns.keys())

            for key, value in setup_dict.items():
                if key != 'id' and key != "cp_id":
                    for x in account:
                        if value:
                            if value == x.id:
                                setup_dict[key] = accou_schema.dump(x)

            return response(200, "Berhasil", True, setup_dict)
            
        return response(200, "Berhasil", False, None)


# Divisi
@app.route("/v1/api/divisi", methods=["POST", "GET"])
@token_required
def divisi(self):
    if request.method == "POST":
        try:
            code = request.json["code"]
            name = request.json["name"]
            desc = request.json["desc"]
            divisi = DivisionMdb(code, name, desc)
            db.session.add(divisi)
            db.session.commit()

            result = response(200, "Berhasil", True, division_schema.dump(divisi))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = DivisionMdb.query.all()

        return response(200, "Berhasil", True, divisions_schema.dump(result))


@app.route("/v1/api/divisi/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def divisi_id(self, id):
    divisi = DivisionMdb.query.filter(DivisionMdb.id == id).first()
    if request.method == "PUT":
        try:
            divisi.code = request.json["code"]
            divisi.name = request.json["name"]
            divisi.desc = request.json["desc"]
            db.session.commit()
            result = response(200, "Berhasil", True, division_schema.dump(divisi))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(divisi)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, division_schema.dump(divisi))