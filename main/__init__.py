import code
from crypt import methods
from fileinput import filename
from math import prod
from pickle import TRUE
import re
from sys import prefix
import time
from unicodedata import name
from datetime import datetime
from flask import Flask, redirect, request, url_for, jsonify, make_response
import requests
from main.function.delete_ap_payment import DeleteApPayment
from main.function.update_ap_giro import UpdateApGiro
from main.function.update_ap_payment import UpdateApPayment
from main.function.update_ar import UpdateAr
from main.function.update_pembelian import UpdatePembelian
from main.function.update_stock import UpdateStock
from main.model.accou_mdb import AccouMdb
from main.model.acq_ddb import AcqDdb
from main.model.adm_menu import AdmMenu
from main.model.adm_user_menu import AdmUserMenu
from main.model.apcard_mdb import ApCard
from main.model.arcard_mdb import ArCard
from main.model.bank_mdb import BankMdb
from main.model.ccost_mdb import CcostMdb
from main.model.comp_mdb import CompMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.exp_ddb import ExpDdb
from main.model.exp_hdb import ExpHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.fmtrl_ddb import FmtrlDdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.fprod_ddb import FprodDdb
from main.model.giro_hdb import GiroHdb
from main.model.hrgbl_mdb import HrgBlMdb
from main.model.jjasa_ddb import JjasaDdb
from main.model.jprod_ddb import JprodDdb
from main.model.msn_mdb import MsnMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.dprod_ddb import DprodDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.jasa_mdb import JasaMdb
from main.model.jpel_mdb import JpelMdb
from main.model.jpem_mdb import JpemMdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.pjasa_ddb import PjasaDdb
from main.model.plan_hdb import PlanHdb
from main.model.plmch_ddb import PlmchDdb
from main.model.po_mdb import PoMdb
from main.model.po_sup_ddb import PoSupDdb
from main.model.pprod_ddb import PprodDdb
from main.model.preq_mdb import PreqMdb
from main.model.prod_mdb import ProdMdb
from main.model.reprod_ddb import ReprodDdb
from main.model.retord_hdb import RetordHdb
from main.model.rjasa_mdb import RjasaMdb
from main.model.rprod_mdb import RprodMdb
from main.model.sales_mdb import SalesMdb
from main.model.area_penjualan_mdb import AreaPenjualanMdb
from main.model.setup_mdb import SetupMdb
from main.model.sjasa_ddb import SjasaDdb
from main.model.sord_hdb import SordHdb
from main.model.sprod_ddb import SprodDdb
from main.model.stcard_mdb import StCard
from main.model.sub_area_mdb import SubAreaMdb
from main.model.klasi_mdb import KlasiMdb
from main.model.kateg_mdb import KategMdb
from main.model.proj_mdb import ProjMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.syarat_bayar_mdb import RulesPayMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.custom_mdb import CustomerMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.unit_mdb import UnitMdb
from main.model.divisi_mdb import DivisionMdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.pajak_mdb import PajakMdb
from main.model.retsale_hdb import RetSaleHdb
from main.model.apcard_mdb import ApCard
from main.model.transddb import TransDdb
from main.model.po_sup_ddb import PoSupDdb
from main.schema.apcard_mdb import apcard_schema, apcards_schema, APCardSchema
from main.schema.arcard_mdb import ARCardSchema
from main.schema.ccost_mdb import ccost_schema, ccosts_schema, CcostSchema
from main.schema.proj_mdb import proj_schema, projs_schema, ProjSchema
from main.shared.shared import db, ma
from main.model.user import User
from main.schema.user import user_schema, users_schema
from main.schema.bank_mdb import banks_schema, bank_schema
from main.schema.unit_mdb import unit_schema, units_schema, UnitSchema
from main.schema.prod_mdb import prod_schema, prods_schema, ProdSchema
from main.schema.po_sup_ddb import poSup_schema, poSups_schema, PoSupSchema
from main.schema.fprdc_hdb import fprdc_schema, fprdcs_schema, FprdcSchema
from main.schema.fprod_ddb import fprod_schema, fprods_schema, FprodSchema
from main.schema.fmtrl_ddb import fmtrl_schema, fmtrls_schema, FmtrlSchema
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
from main.schema.group_prod_mdb import groupPro_schema, groupPros_schema
from main.schema.pajak_mdb import pajk_schema, pajks_schema
from main.schema.jasa_mdb import jasa_schema, jasas_schema
from main.schema.preq_mdb import preq_schema, preqs_schema, PreqSchema
from main.schema.rprod_mdb import rprod_schema, rprods_schema, RprodSchema
from main.schema.rjasa_mdb import rjasa_schema, rjasas_schema, RjasaSchema
from main.schema.pprod_ddb import pprod_schema, pprods_schema, PprodSchema
from main.schema.pjasa_ddb import pjasa_schema, pjasas_schema, PjasaSchema
from main.schema.sprod_ddb import sprod_schema, sprods_schema, SprodSchema
from main.schema.sjasa_ddb import sjasa_schema, sjasas_schema, SjasaSchema
from main.schema.po_mdb import po_schema, pos_schema, PoSchema
from main.schema.sord_hdb import sord_schema, sords_schema, SordSchema
from main.schema.dord_hdb import dord_schema, dords_schema, DordSchema
from main.schema.dprod_ddb import dprod_schema, dprods_schema, DprodSchema
from main.schema.djasa_ddb import djasa_schema, djasas_schema, DjasaSchema
from main.schema.fkpb_hdb import fkpbs_schema, fkpb_schema, FkpbSchema
from main.schema.retord_hdb import retord_schema, retords_schema, RetordSchema
from main.schema.reprod_ddb import reprod_schema, reprods_schema, ReprodSchema
from main.schema.ordpj_hdb import ordpj_schema, ordpjs_schema, OrdpjSchema
from main.schema.jprod_ddb import jprod_schema, jprods_schema, JprodSchema
from main.schema.jjasa_ddb import jjasa_schema, jjasas_schema, JjasaSchema
from main.schema.exp_hdb import exp_schema, exps_schema, ExpSchema
from main.schema.dexp_ddb import dexp_schema, dexps_schema, DexpSchema
from main.schema.dacq_ddb import dacq_schema, dacqs_schema, DacqSchema
from main.schema.acq_ddb import acq_schema, acqs_schema, AcqSchema
from main.schema.giro_hdb import giro_schema, giros_schema, GiroSchema
from main.schema.apcard_mdb import apcard_schema, apcards_schema, APCardSchema
from main.schema.retsale_hdb import retsale_schema, retsales_schema, RetSaleSchema
from main.schema.transddb import trans_schema, transs_schema, TransDDB
from main.schema.stcard_mdb import st_card_schema, st_cards_schema, StCardSchema
from main.schema.msn_mdb import msns_schema, msn_schema, MsnSchema
from main.schema.plan_hdb import plan_schema, plans_schema, PlanSchema
from main.schema.plmch_ddb import plmch_schema, plmchs_schema, PlmchSchema
from main.schema.setup_mdb import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, extract, func, or_
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
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
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
            return result
    else:
        result = (
            db.session.query(BankMdb, AccouMdb)
            .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
            .order_by(BankMdb.id.asc())
            .all()
        )
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
        bank.BANK_NAME = request.json["BANK_NAME"]
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
        if "acc_code" in request.json:
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
            return response(406, "Data isian belum lengkap", False, None)
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
        sub_cus = request.json["sub_cus"]
        cus_id = request.json["cus_id"]
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
                sub_cus,
                cus_id,
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
            db.session.query(CustomerMdb, JpelMdb, SubAreaMdb, CurrencyMdb, PajakMdb)
            .outerjoin(JpelMdb, JpelMdb.id == CustomerMdb.cus_jpel)
            .outerjoin(SubAreaMdb, SubAreaMdb.id == CustomerMdb.cus_sub_area)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == CustomerMdb.cus_curren)
            .outerjoin(PajakMdb, PajakMdb.id == CustomerMdb.cus_pjk)
            .order_by(JpelMdb.id.asc())
            .order_by(CurrencyMdb.id.asc())
            .order_by(CustomerMdb.cus_code.asc())
            .all()
        )

        for x in result:
            if x[0].sub_cus:
                for y in result:
                    if x[0].cus_id == y[0].id:
                        x[0].cus_id = customer_schema.dump(y[0])

        data = [
            {
                "customer": customer_schema.dump(x[0]),
                "jpel": jpel_schema.dump(x[1]),
                "subArea": sub_area_schema.dump(x[2]),
                "currency": currency_schema.dump(x[3]),
                "pajak": pajk_schema.dump(x[4]),
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
        customer.cus_sub = request.json["sub_cus"]
        customer.cus_id = request.json["cus_id"] if request.json["sub_cus"] else None
        db.session.commit()

        return response(200, "Berhasil", True, customer_schema.dump(customer))
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        cus = CustomerMdb.query.all()

        result = (
            db.session.query(CustomerMdb, JpelMdb, SubAreaMdb, CurrencyMdb, PajakMdb)
            .outerjoin(JpelMdb, JpelMdb.id == CustomerMdb.cus_jpel)
            .outerjoin(SubAreaMdb, SubAreaMdb.id == CustomerMdb.cus_sub_area)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == CustomerMdb.cus_curren)
            .outerjoin(PajakMdb, PajakMdb.id == CustomerMdb.cus_pjk)
            .order_by(CustomerMdb.cus_code.asc())
            .filter(CustomerMdb.id == id)
            .first()
        )

        if result[0].sub_cus:
            for y in cus:
                if result[0].cus_id == y[0].id:
                    result[0].cus_id = customer_schema.dump(y[0])

        data = {
            "customer": customer_schema.dump(result[0]),
            "jpel": jpel_schema.dump(result[1]),
            "subArea": sub_area_schema.dump(result[2]),
            "currency": currency_schema.dump(result[3]),
            "pajak": pajk_schema.dump(result[4]),
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
            sto_general = request.json["sto_general"]
            sto_production = request.json["sto_production"]
            sto_wip = request.json["sto_wip"]
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
                sto_wip,
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

        if setup:
            setup_dict = dict(
                (col, getattr(setup, col)) for col in setup.__table__.columns.keys()
            )

            for key, value in setup_dict.items():
                if key != "id" and key != "cp_id":
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
        setup.sto_general = request.json["sto_general"]
        setup.sto_production = request.json["sto_production"]
        setup.sto_hpp_diff = request.json["sto_hpp_diff"]
        setup.sto_wip = request.json["sto_wip"]
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
            setup_dict = dict(
                (col, getattr(setup, col)) for col in setup.__table__.columns.keys()
            )

            for key, value in setup_dict.items():
                if key != "id" and key != "cp_id":
                    for x in account:
                        if value:
                            if value == x.id:
                                setup_dict[key] = accou_schema.dump(x)

            return response(200, "Berhasil", True, setup_dict)

        return response(200, "Berhasil", False, None)


@app.route("/v1/api/unit", methods=["POST", "GET"])
@token_required
def unit(self):
    units = UnitMdb.query.order_by(UnitMdb.id.asc()).all()
    if request.method == "POST":
        code = request.json["code"]
        name = request.json["name"]
        type = request.json["type"]
        desc = request.json["desc"]
        active = request.json["active"]
        qty = request.json["qty"]
        u_from = request.json["u_from"]
        u_to = request.json["u_to"]

        try:
            if "konversi" in request.json:
                konversi = request.json["konversi"]
                u = []
                for x in konversi:
                    if x["u_from"] and x["u_to"]:
                        u.append(
                            UnitMdb(
                                code,
                                name,
                                type,
                                desc,
                                active,
                                x["qty"],
                                x["u_from"],
                                x["u_to"],
                            )
                        )
                if len(u) > 0:
                    db.session.add_all(u)
                    db.session.commit()
                    result = response(200, "Berhasil", True, units_schema.dump(u))
                else:
                    u = UnitMdb(code, name, type, desc, active, qty, u_from, u_to)
                    db.session.add(u)
                    db.session.commit()
                    result = response(200, "Berhasil", True, unit_schema.dump(u))
        except IntegrityError:
            db.session.rollback()
            result = response(
                400, "Kode satuan " + code + " sudah digunakan", False, None
            )
        finally:
            return result
    else:
        for x in units:
            if x.type == "k" and x.u_from:
                for y in units:
                    if x.u_from == y.id:
                        x.u_from = UnitSchema(only=["id", "code", "name"]).dump(y)
            if x.type == "k" and x.u_to:
                for y in units:
                    if x.u_to == y.id:
                        x.u_to = UnitSchema(only=["id", "code", "name"]).dump(y)

        return response(200, "Berhasil", True, units_schema.dump(units))


@app.route("/v1/api/unit-konversi", methods=["POST"])
@token_required
def unit_convert(self):
    konversi = request.json["konversi"]
    u = []
    for x in konversi:
        if x["code"] and x["qty"] and x["u_from"] and x["u_to"]:
            u.append(
                UnitMdb(
                    x["code"],
                    x["code"],
                    "k",
                    None,
                    True,
                    x["qty"],
                    x["u_from"],
                    x["u_to"],
                )
            )

    db.session.add_all(u)
    db.session.commit()

    return response(200, "Berhasil", True, units_schema.dump(u))


@app.route("/v1/api/unit/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def satuan_id(self, id):
    units = UnitMdb.query.filter(UnitMdb.id == id).first()
    result = UnitMdb.query.all()
    if request.method == "PUT":
        code = request.json["code"]
        name = request.json["name"]
        type = request.json["type"]
        desc = request.json["desc"]
        active = request.json["active"]

        old_ids = []
        new_unit = []
        if "konversi" in request.json:
            konversi = request.json["konversi"]
            for x in konversi:
                if x["u_from"] and x["u_to"]:
                    if x["id"] != 0:
                        old_ids.append(x["id"])
                    else:
                        new_unit.append(
                            UnitMdb(
                                code,
                                name,
                                type,
                                desc,
                                active,
                                x["qty"],
                                x["u_from"],
                                x["u_to"],
                            )
                        )
            if len(old_ids) > 0:
                old_units = (
                    db.session.query(UnitMdb).filter(UnitMdb.id.in_(old_ids)).all()
                )
                for x in old_units:
                    x.code = code
                    x.name = name
                    x.type = type
                    x.desc = desc
                    x.active = active
                    for y in konversi:
                        if y["id"] == x.id:
                            x.qty = y["qty"]
                            x.u_from = y["u_from"]
                            x.u_to = y["u_to"]

            if len(new_unit) > 0:
                db.session.add_all(new_unit)

            if len(new_unit) == 0 and len(old_ids) == 0:
                units.code = code
                units.name = name
                units.type = type
                units.desc = desc
                units.active = active
                units.qty = request.json["qty"]
                units.u_from = request.json["u_from"]
                units.u_to = request.json["u_to"]

            db.session.commit()

        return response(200, "Berhasil", True, unit_schema.dump(units))
    elif request.method == "DELETE":
        db.session.delete(units)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        x = units
        if x.type == "k" and x.u_from:
            for y in result:
                if x.u_from == y.id:
                    x.u_from = UnitSchema(only=["id", "code", "name"]).dump(y)
        if x.type == "k" and x.u_to:
            for y in result:
                if x.u_to == y.id:
                    x.u_to = UnitSchema(only=["id", "code", "name"]).dump(y)

        return response(200, "Berhasil", True, unit_schema.dump(units))


@app.route("/v1/api/product", methods=["POST", "GET"])
@token_required
def product(self):
    if request.method == "POST":
        try:
            code = request.json["code"]
            name = request.json["name"]
            group = request.json["group"]
            type = request.json["type"]
            codeb = request.json["codeb"]
            unit = request.json["unit"]
            suplier = request.json["suplier"]
            b_price = request.json["b_price"]
            s_price = request.json["s_price"]
            barcode = request.json["barcode"]
            metode = request.json["metode"]
            max_stock = request.json["max_stock"]
            min_stock = request.json["min_stock"]
            re_stock = request.json["re_stock"]
            lt_stock = request.json["lt_stock"]
            max_order = request.json["max_order"]
            image = request.json["image"]

            prod = ProdMdb(
                code,
                name,
                group,
                type,
                codeb,
                unit,
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
            )
            db.session.add(prod)
            db.session.commit()

            result = response(200, "Berhasil", True, prod_schema.dump(prod))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = (
            db.session.query(ProdMdb, SupplierMdb, UnitMdb, GroupProMdb)
            .outerjoin(SupplierMdb, SupplierMdb.id == ProdMdb.suplier)
            .outerjoin(UnitMdb, UnitMdb.id == ProdMdb.unit)
            .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
            .order_by(ProdMdb.id.asc())
            .all()
        )

        data = []

        if result:
            for x in result:
                x[0].image = (
                    request.host_url + "static/upload/" + x[0].image
                    if x[0].image and x[0].image != ""
                    else None
                )
                x[0].suplier = supplier_schema.dump(x[1]) if x[1] else None
                x[0].unit = unit_schema.dump(x[2]) if x[2] else None
                x[0].group = groupPro_schema.dump(x[3]) if x[3] else None
                data.append(prod_schema.dump(x[0]))

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/product/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def product_id(self, id):
    prod = ProdMdb.query.filter(ProdMdb.id == id).first()
    if request.method == "PUT":
        try:
            prod.code = request.json["code"]
            prod.name = request.json["name"]
            prod.group = request.json["group"]
            prod.type = request.json["type"]
            prod.codeb = request.json["codeb"]
            prod.unit = request.json["unit"]
            prod.suplier = request.json["suplier"]
            prod.b_price = request.json["b_price"]
            prod.s_price = request.json["s_price"]
            prod.barcode = request.json["barcode"]
            prod.metode = request.json["metode"]
            prod.max_stock = request.json["max_stock"]
            prod.min_stock = request.json["min_stock"]
            prod.re_stock = request.json["re_stock"]
            prod.lt_stock = request.json["lt_stock"]
            prod.max_order = request.json["max_order"]

            if request.host_url + "static/upload/" in request.json["image"]:
                image = request.json["image"].replace(
                    request.host_url + "static/upload/", ""
                )
            else:
                image = request.json["image"]

            if prod.image != image:
                if prod.image != "" and prod.image is not None:
                    if os.path.exists(
                        os.path.join(app.config["UPLOAD_FOLDER"], prod.image)
                    ):
                        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], prod.image))

            prod.image = image

            db.session.commit()

            result = response(200, "Berhasil", True, prod_schema.dump(prod))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(prod)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        prod.image = (
            request.host_url + "static/upload/" + prod.image
            if prod.image and prod.image != ""
            else None
        )
        return response(200, "Berhasil", True, prod_schema.dump(prod))


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


@app.route("/v1/api/group-product", methods=["POST", "GET"])
@token_required
def groupPro(self):
    if request.method == "POST":
        code = request.json["code"]
        name = request.json["name"]
        div_code = request.json["div_code"]
        acc_sto = request.json["acc_sto"]
        acc_send = request.json["acc_send"]
        acc_terima = request.json["acc_terima"]
        hrg_pokok = request.json["hrg_pokok"]
        acc_penj = request.json["acc_penj"]
        potongan = request.json["potongan"]
        pengembalian = request.json["pengembalian"]
        selisih = request.json["selisih"]
        try:
            groupPro = GroupProMdb(
                code,
                name,
                div_code,
                acc_sto,
                acc_send,
                acc_terima,
                hrg_pokok,
                acc_penj,
                potongan,
                pengembalian,
                selisih,
            )
            db.session.add(groupPro)
            db.session.commit()
            result = response(200, "Berhasil", True, groupPro_schema.dump(groupPro))
        except IntegrityError:
            db.session.rollback()
            result = response(
                400, "Kode akun " + code + " sudah digunakan", False, None
            )
        finally:
            return result
    else:
        result = (
            db.session.query(GroupProMdb, DivisionMdb)
            .outerjoin(DivisionMdb, DivisionMdb.id == GroupProMdb.div_code)
            .order_by(GroupProMdb.id.asc())
            .all()
        )
        data = [
            {
                "groupPro": groupPro_schema.dump(x[0]),
                "divisi": division_schema.dump(x[1]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/group-product/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def groupPro_id(self, id):
    groupPro = GroupProMdb.query.filter(GroupProMdb.id == id).first()
    if request.method == "PUT":
        groupPro.code = request.json["code"]
        groupPro.name = request.json["name"]
        groupPro.div_code = request.json["div_code"]
        groupPro.acc_sto = request.json["acc_sto"]
        groupPro.acc_send = request.json["acc_send"]
        groupPro.acc_terima = request.json["acc_terima"]
        groupPro.hrg_pokok = request.json["hrg_pokok"]
        groupPro.acc_penj = request.json["acc_penj"]
        groupPro.potongan = request.json["potongan"]
        groupPro.pengembalian = request.json["pengembalian"]
        groupPro.selisih = request.json["selisih"]
        db.session.commit()

        return response(200, "Berhasil", True, groupPro_schema.dump(groupPro))
    elif request.method == "DELETE":
        db.session.delete(groupPro)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(GroupProMdb, DivisionMdb)
            .join(DivisionMdb, DivisionMdb.id == GroupProMdb.div_code)
            .order_by(GroupProMdb.div_code.asc())
            .filter(GroupProMdb.id == id)
            .first()
        )

        data = {
            "groupPro": groupPro_schema.dump(result[0]),
            "divisi": division_schema.dump(result[1]),
        }

        return response(200, "Berhasil", True, data)


# Pajak
@app.route("/v1/api/pajak", methods=["POST", "GET"])
@token_required
def pajak(self):
    if request.method == "POST":
        try:
            type = request.json["type"]
            name = request.json["name"]
            nilai = request.json["nilai"]
            cutting = request.json["cutting"]
            acc_sls_tax = request.json["acc_sls_tax"]
            acc_pur_tax = request.json["acc_pur_tax"]
            combined = request.json["combined"]
            pajak = PajakMdb(
                type, name, nilai, cutting, acc_sls_tax, acc_pur_tax, combined
            )
            db.session.add(pajak)
            db.session.commit()

            result = response(200, "Berhasil", True, pajk_schema.dump(pajak))
        finally:
            return result
    else:
        result = PajakMdb.query.all()

        return response(200, "Berhasil", True, pajks_schema.dump(result))


@app.route("/v1/api/pajak/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def pajak_id(self, id):
    pajak = PajakMdb.query.filter(PajakMdb.id == id).first()
    if request.method == "PUT":
        try:
            pajak.type = request.json["type"]
            pajak.name = request.json["name"]
            pajak.nilai = request.json["nilai"]
            pajak.cutting = request.json["cutting"]
            pajak.acc_sls_tax = request.json["acc_sls_tax"]
            pajak.acc_pur_tax = request.json["acc_pur_tax"]
            pajak.combined = request.json["combined"]
            db.session.commit()
            result = response(200, "Berhasil", True, pajk_schema.dump(pajak))
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(pajak)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        return response(200, "Berhasil", True, pajk_schema.dump(pajak))


# Jasa
@app.route("/v1/api/jasa", methods=["POST", "GET"])
@token_required
def jasa(self):
    if request.method == "POST":
        try:
            code = request.json["code"]
            name = request.json["name"]
            desc = request.json["desc"]
            acc_id = request.json["acc_id"]
            jasa = JasaMdb(code, name, desc, acc_id)
            db.session.add(jasa)
            db.session.commit()

            result = response(200, "Berhasil", True, jasa_schema.dump(jasa))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        result = (
            db.session.query(JasaMdb, AccouMdb)
            .outerjoin(AccouMdb, AccouMdb.id == JasaMdb.acc_id)
            .order_by(JasaMdb.id.asc())
            .all()
        )

        data = [
            {
                "jasa": jasa_schema.dump(x[0]),
                "account": accou_schema.dump(x[1]),
            }
            for x in result
        ]

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/jasa/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def jasa_id(self, id):
    jasa = JasaMdb.query.filter(JasaMdb.id == id).first()
    if request.method == "PUT":
        try:
            jasa.code = request.json["code"]
            jasa.name = request.json["name"]
            jasa.desc = request.json["desc"]
            jasa.acc_id = request.json["acc_id"]
            db.session.commit()
            result = response(200, "Berhasil", True, jasa_schema.dump(jasa))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        db.session.delete(jasa)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(JasaMdb, AccouMdb)
            .outerjoin(AccouMdb, AccouMdb.id == JasaMdb.acc_id)
            .order_by(JasaMdb.id.asc())
            .filter(JasaMdb.id == id)
            .first()
        )

        data = {
            "jasa": jasa_schema.dump(result[0]),
            "account": accou_schema.dump(result[1]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/rp", methods=["POST", "GET"])
@token_required
def rp(self):
    if request.method == "POST":
        try:
            req_code = request.json["req_code"]
            req_date = request.json["req_date"]
            req_dep = request.json["req_dep"]
            req_ket = request.json["req_ket"]
            refrence = request.json["refrence"]
            ref_sup = request.json["ref_sup"]
            ref_ket = request.json["ref_ket"]

            rp = PreqMdb(
                req_code, req_date, req_dep, req_ket, refrence, ref_sup, ref_ket, 0
            )
            db.session.add(rp)
            db.session.commit()

            rprod = request.json["rprod"]
            all_prod = []
            for x in rprod:
                if x["prod_id"] and x["unit_id"] and x["request"]:
                    all_prod.append(
                        RprodMdb(
                            rp.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["request"],
                            x["request"],
                        )
                    )

            if len(all_prod) > 0:
                db.session.add_all(all_prod)

            rjasa = request.json["rjasa"]
            all_jasa = []
            for x in rjasa:
                if x["jasa_id"] and x["request"] and x["unit_id"]:
                    all_jasa.append(
                        RjasaMdb(
                            rp.id,
                            x["jasa_id"],
                            x["unit_id"],
                            x["request"],
                            x["request"],
                        )
                    )

            if len(all_jasa) > 0:
                db.session.add_all(all_jasa)

            db.session.commit()

            result = response(200, "Berhasil", True, preq_schema.dump(rp))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        preq = (
            db.session.query(PreqMdb, CcostMdb, SupplierMdb)
            .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
            .outerjoin(SupplierMdb, SupplierMdb.id == PreqMdb.ref_sup)
            .order_by(PreqMdb.id.asc())
            .all()
        )
        rprod = (
            db.session.query(RprodMdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == RprodMdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == RprodMdb.unit_id)
            .all()
        )
        rjasa = (
            db.session.query(RjasaMdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == RjasaMdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == RjasaMdb.unit_id)
            .all()
        )

        final = []

        for x in preq:
            product = []
            for y in rprod:
                if y[0].preq_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    product.append(rprod_schema.dump(y[0]))

            jasa = []
            for z in rjasa:
                if z[0].preq_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(rjasa_schema.dump(z[0]))

            final.append(
                {
                    "id": x[0].id,
                    "req_code": x[0].req_code,
                    "req_date": PreqSchema(only=["req_date"]).dump(x[0])["req_date"],
                    "req_dep": ccost_schema.dump(x[1]) if x[1] else None,
                    "req_ket": x[0].req_ket,
                    "refrence": x[0].refrence,
                    "ref_sup": supplier_schema.dump(x[2]) if x[2] else None,
                    "ref_ket": x[0].ref_ket,
                    "status": x[0].status,
                    "rprod": product,
                    "rjasa": jasa,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/rp/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def rp_id(self, id):
    preq = PreqMdb.query.filter(PreqMdb.id == id).first()
    product = RprodMdb.query.filter(RprodMdb.preq_id == id).all()
    jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == id).all()
    if request.method == "PUT":
        if preq.status == 0:
            req_code = request.json["req_code"]
            req_date = request.json["req_date"]
            req_dep = request.json["req_dep"]
            req_ket = request.json["req_ket"]
            refrence = request.json["refrence"]
            ref_sup = request.json["ref_sup"]
            ref_ket = request.json["ref_ket"]
            rprod = request.json["rprod"]
            rjasa = request.json["rjasa"]

            preq.req_code = req_code
            preq.req_date = req_date
            preq.req_dep = req_dep
            preq.req_ket = req_ket
            preq.refrence = refrence
            preq.ref_sup = ref_sup
            preq.ref_ket = ref_ket

            old_prod = []
            new_prod = []

            for x in rprod:
                if x["prod_id"] and x["unit_id"] and x["request"]:
                    if x["id"] != 0:
                        old_prod.append(x["id"])
                    else:
                        new_prod.append(
                            RprodMdb(
                                preq.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["request"],
                                x["request"],
                            )
                        )

            if len(old_prod) > 0:
                for x in old_prod:
                    for y in product:
                        if y.id not in old_prod:
                            db.session.delete(y)
                        else:
                            if y.id == x:
                                for z in rprod:
                                    if z["id"] == x:
                                        y.prod_id = z["prod_id"]
                                        y.unit_id = z["unit_id"]
                                        y.request = z["request"]

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            old_jasa = []
            new_jasa = []

            for x in rjasa:
                if x["jasa_id"] and x["qty"] and x["unit_id"]:
                    if x["id"] != 0:
                        old_jasa.append(x["id"])
                    else:
                        new_jasa.append(
                            RjasaMdb(
                                preq.id,
                                None,
                                x["jasa_id"],
                                x["unit_id"],
                                x["qty"],
                                None,
                                None,
                                None,
                            )
                        )

            if len(old_jasa) > 0:
                for x in old_jasa:
                    for y in jasa:
                        if y.id not in old_jasa:
                            db.session.delete(y)
                        else:
                            if y.id == x:
                                for z in rjasa:
                                    if z["id"] == x:
                                        y.jasa_id = z["jasa_id"]
                                        y.unit_id = z["unit_id"]
                                        y.qty = z["qty"]

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            preq = PreqMdb.query.filter(PreqMdb.id == id).first()
            product = RprodMdb.query.filter(RprodMdb.preq_id == id).all()
            jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == id).all()
            final = {
                "id": preq.id,
                "req_code": preq.req_code,
                "req_date": preq.req_date,
                "req_dep": preq.req_dep,
                "req_ket": preq.req_ket,
                "refrence": preq.refrence,
                "ref_sup": preq.ref_sup,
                "ref_ket": preq.ref_ket,
                "status": preq.status,
                "rprod": rprods_schema.dump(product),
                "rjasa": rjasas_schema.dump(jasa),
            }

            return response(200, "Berhasil", True, final)
        else:
            return response(400, "Tidak dapat mengedit karena status", False, None)
    elif request.method == "DELETE":
        if preq:
            if preq.status == 0:
                db.session.delete(preq)
                for x in product:
                    db.session.delete(x)
                for x in jasa:
                    db.session.delete(x)
                db.session.commit()
                return response(200, "Berhasil", True, None)

        return response(
            400, "Tidak dapat mengedit karena status tidak open", False, None
        )
    else:
        preq = (
            db.session.query(PreqMdb, CcostMdb, SupplierMdb)
            .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
            .outerjoin(SupplierMdb, SupplierMdb.id == PreqMdb.ref_sup)
            .filter(PreqMdb.id == id)
            .first()
        )

        rprod = (
            db.session.query(RprodMdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == RprodMdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == RprodMdb.unit_id)
            .filter(RprodMdb.preq_id == id)
            .all()
        )

        rjasa = (
            db.session.query(RjasaMdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == RjasaMdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == RjasaMdb.unit_id)
            .filter(RjasaMdb.preq_id == id)
            .all()
        )

        prods = []
        for y in rprod:
            y[0].prod_id = prod_schema.dump(y[1])
            y[0].unit_id = unit_schema.dump(y[2])
            prods.append(rprod_schema.dump(y[0]))

        jasas = []
        for z in rjasa:
            z[0].jasa_id = jasa_schema.dump(z[1])
            z[0].unit_id = unit_schema.dump(z[2])
            jasas.append(rjasa_schema.dump(z[0]))

        final = {
            "id": preq[0].id,
            "req_code": preq[0].req_code,
            "req_date": preq[0].req_date,
            "req_dep": preq[0].req_dep,
            "req_ket": preq[0].req_ket,
            "refrence": preq[0].refrence,
            "ref_sup": preq[0].ref_sup,
            "ref_ket": preq[0].ref_ket,
            "status": preq[0].status,
            "rprod": prods,
            "rjasa": jasas,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/po", methods=["POST", "GET"])
@token_required
def po(self):
    if request.method == "POST":
        try:
            po_code = request.json["po_code"]
            po_date = request.json["po_date"]
            preq_id = request.json["preq_id"]
            sup_id = request.json["sup_id"]
            ref_sup = request.json["ref_sup"]
            ppn_type = request.json["ppn_type"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            pprod = request.json["pprod"]
            pjasa = request.json["pjasa"]
            psup = request.json["psup"]

            po = PoMdb(
                po_code,
                po_date,
                preq_id,
                sup_id,
                ref_sup,
                ppn_type,
                top,
                due_date,
                split_inv,
                prod_disc,
                jasa_disc,
                total_disc,
                0,
                0,
                0,
            )

            db.session.add(po)
            db.session.commit()

            preq = PreqMdb.query.filter(PreqMdb.id == preq_id).first()

            product = RprodMdb.query.filter(RprodMdb.preq_id == preq_id).all()
            jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == preq_id).all()

            new_prod = []
            for x in pprod:
                for y in product:
                    if x["id"] == y.id:
                        y.remain = y.remain - int(x["order"])
                if (
                    x["prod_id"]
                    and x["unit_id"]
                    and x["order"]
                    and int(x["order"]) > 0
                    and x["price"]
                    and int(x["price"]) > 0
                ):
                    new_prod.append(
                        PprodDdb(
                            po.id,
                            preq_id,
                            x["id"] if x["id"] != 0 else None,
                            x["prod_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in pjasa:
                for y in jasa:
                    if x["id"] == y.id:
                        y.remain = y.remain - int(x["order"])
                if (
                    x["sup_id"]
                    and x["jasa_id"]
                    and x["unit_id"]
                    and x["order"]
                    and int(x["order"]) > 0
                    and x["price"]
                    and int(x["price"]) > 0
                ):
                    new_jasa.append(
                        PjasaDdb(
                            po.id,
                            preq_id,
                            x["id"] if x["id"] != 0 else None,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            new_sup = []
            print(psup)
            for x in psup:
                if (
                    x["sup_id"]
                    and x["prod_id"]
                    and x["price"]
                    and int(x["price"]) > 0
                    # and x["image"]
                ):
                    new_sup.append(
                        PoSupDdb(
                            po.id, x["sup_id"], x["prod_id"], x["price"], x["image"]
                        )
                    )
            print(new_sup)
            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            if len(new_sup) > 0:
                db.session.add_all(new_sup)

            db.session.commit()

            # status == 0 : belum ada po
            # status == 1 : sudah ada po, tapi produk/jasa masih sisa
            # status == 2 : selesai
            remain = 0
            for x in product:
                remain += x.remain
            for x in jasa:
                remain += x.remain
            if remain == 0:
                preq.status = 2
            else:
                preq.status = 1

            db.session.commit()

            result = response(200, "Berhasil", True, po_schema.dump(po))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        po = (
            db.session.query(PoMdb, PreqMdb, CcostMdb, SupplierMdb, RulesPayMdb)
            .outerjoin(PreqMdb, PreqMdb.id == PoMdb.preq_id)
            .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
            .outerjoin(SupplierMdb, SupplierMdb.id == PoMdb.sup_id)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == PoMdb.top)
            .order_by(PoMdb.id.desc())
            .all()
        )

        pprod = (
            db.session.query(PprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == PprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == PprodDdb.unit_id)
            .all()
        )

        pjasa = (
            db.session.query(PjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == PjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == PjasaDdb.unit_id)
            .all()
        )
        psup = (
            db.session.query(PoSupDdb, SupplierMdb, ProdMdb)
            .outerjoin(SupplierMdb, SupplierMdb.id == PoSupDdb.sup_id)
            .outerjoin(ProdMdb, ProdMdb.id == PoSupDdb.prod_id)
            .all()
        )

        final = []
        for x in po:
            product = []
            for y in pprod:
                if y[0].po_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    product.append(pprod_schema.dump(y[0]))

            jasa = []
            for z in pjasa:
                if z[0].po_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(pjasa_schema.dump(z[0]))

            sup = []
            for z in psup:
                if z[0].po_id == x[0].id:
                    z[0].sup_id = supplier_schema.dump(z[1])
                    z[0].prod_id = prod_schema.dump(z[2])
                    sup.append(poSup_schema.dump(z[0]))

            final.append(
                {
                    "id": x[0].id,
                    "po_code": x[0].po_code,
                    "po_date": PoSchema(only=["po_date"]).dump(x[0])["po_date"],
                    "preq_id": {
                        "id": x[1].id,
                        "req_code": x[1].req_code,
                        "req_date": PreqSchema(only=["req_date"]).dump(x[1])[
                            "req_date"
                        ],
                        "req_dep": ccost_schema.dump(x[2]) if x[2] else None,
                        "req_ket": x[1].req_ket,
                        "status": x[1].status,
                    }
                    if x[1]
                    else None,
                    "ppn_type": x[0].ppn_type,
                    "sup_id": supplier_schema.dump(x[3]) if x[3] else None,
                    "ref_sup": x[0].ref_sup,
                    "top": rpay_schema.dump(x[4]) if x[4] else None,
                    "due_date": PoSchema(only=["due_date"]).dump(x[0])["due_date"]
                    if x[0].due_date
                    else None,
                    "split_inv": x[0].split_inv,
                    "prod_disc": x[0].prod_disc,
                    "jasa_disc": x[0].jasa_disc,
                    "total_disc": x[0].total_disc,
                    "status": x[0].status,
                    "apprv": x[0].apprv,
                    "print": x[0].print,
                    "pprod": product,
                    "pjasa": jasa,
                    "psup": sup,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/po/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def po_id(self, id):
    po = PoMdb.query.filter(PoMdb.id == id).first()
    if request.method == "PUT":
        if po.print == 0 and po.status == 0:
            try:
                po_code = request.json["po_code"]
                po_date = request.json["po_date"]
                preq_id = request.json["preq_id"]
                sup_id = request.json["sup_id"]
                ref_sup = request.json["ref_sup"]
                ppn_type = request.json["ppn_type"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                pprod = request.json["pprod"]
                pjasa = request.json["pjasa"]

                po.po_code = po_code
                po.po_date = po_date
                po.preq_id = preq_id
                po.sup_id = sup_id
                po.ref_sup = ref_sup
                po.ppn_type = ppn_type
                po.top = top
                po.due_date = due_date
                po.split_inv = split_inv
                po.prod_disc = prod_disc
                po.jasa_disc = jasa_disc
                po.total_disc = total_disc

                preq = PreqMdb.query.filter(PreqMdb.id == preq_id).first()

                product = RprodMdb.query.filter(RprodMdb.preq_id == po.preq_id).all()
                jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == po.preq_id).all()
                old_prod = PprodDdb.query.filter(PprodDdb.preq_id == po.preq_id).all()
                old_jasa = PjasaDdb.query.filter(PjasaDdb.preq_id == po.preq_id).all()

                new_prod = []
                for x in pprod:
                    for y in product:
                        if x["rprod_id"] == y.id:
                            for z in old_prod:
                                if x["id"] == z.id:
                                    y.remain = z.order - int(x["order"]) + y.remain
                                    z.prod_id = x["prod_id"]
                                    z.unit_id = x["unit_id"]
                                    z.order = x["order"]
                                    z.price = x["price"]
                                    z.nett_price = x["nett_price"]
                                    z.disc = x["disc"]
                                    z.total = x["total"]
                    if (
                        x["id"] == 0
                        and x["prod_id"]
                        and x["unit_id"]
                        and x["order"]
                        and int(x["order"]) > 0
                        and x["price"]
                        and int(x["price"]) > 0
                    ):
                        new_prod.append(
                            PprodDdb(
                                po.id,
                                preq_id,
                                None if x["id"] != 0 else None,
                                x["prod_id"],
                                x["unit_id"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["nett_price"],
                                x["total"],
                            )
                        )

                new_jasa = []
                for x in pjasa:
                    for y in jasa:
                        if x["rjasa_id"] == y.id:
                            for z in old_jasa:
                                if x["id"] == z.id:
                                    y.remain = z.order - int(x["order"]) + y.remain
                                    z.sup_id = x["sup_id"]
                                    z.jasa_id = x["prod_id"]
                                    z.unit_id = x["unit_id"]
                                    z.order = x["order"]
                                    z.price = x["price"]
                                    z.disc = x["disc"]
                                    z.total = x["total"]
                    if (
                        x["id"] == 0
                        and x["sup_id"]
                        and x["jasa_id"]
                        and x["unit_id"]
                        and x["order"]
                        and int(x["order"]) > 0
                        and x["price"]
                        and int(x["price"]) > 0
                    ):
                        new_jasa.append(
                            PjasaDdb(
                                po.id,
                                preq_id,
                                None if x["id"] != 0 else None,
                                x["sup_id"],
                                x["jasa_id"],
                                x["unit_id"],
                                x["order"],
                                x["price"],
                                x["disc"],
                                x["total"],
                            )
                        )

                if len(new_prod) > 0:
                    db.session.add_all(new_prod)

                if len(new_jasa) > 0:
                    db.session.add_all(new_jasa)

                db.session.commit()

                remain = 0
                for x in product:
                    remain += x.remain
                for x in jasa:
                    remain += x.remain
                if remain == 0:
                    preq.status = 2
                else:
                    preq.status = 1

                db.session.commit()

                result = response(200, "Berhasil", True, po_schema.dump(po))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result

    elif request.method == "DELETE":
        if po.status == 0:
            product = RprodMdb.query.filter(RprodMdb.preq_id == po.preq_id).all()
            jasa = RjasaMdb.query.filter(RjasaMdb.preq_id == po.preq_id).all()
            pprod = PprodDdb.query.filter(PprodDdb.po_id == po.id).all()
            pjasa = PjasaDdb.query.filter(PjasaDdb.po_id == po.id).all()

            for y in product:
                for z in pprod:
                    if z.rprod_id == y.id:
                        y.remain += z.order
                    db.session.delete(z)

            for y in jasa:
                for z in pjasa:
                    if z.rjasa_id == y.id:
                        y.remain += z.order
                    db.session.delete(z)

            db.session.delete(po)
            db.session.commit()
            return response(200, "Berhasil", True, None)
    else:
        x = (
            db.session.query(PoMdb, PreqMdb, CcostMdb, SupplierMdb, RulesPayMdb)
            .outerjoin(PreqMdb, PreqMdb.id == PoMdb.preq_id)
            .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
            .outerjoin(SupplierMdb, SupplierMdb.id == PoMdb.sup_id)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == PoMdb.top)
            .filter(PoMdb.id == id)
            .first()
        )

        pprod = (
            db.session.query(PprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == PprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == PprodDdb.unit_id)
            .all()
        )

        pjasa = (
            db.session.query(PjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == PjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == PjasaDdb.unit_id)
            .all()
        )

        product = []
        for y in pprod:
            if y[0].po_id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                product.append(pprod_schema.dump(y[0]))

        jasa = []
        for z in pjasa:
            if z[0].po_id == x[0].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(pjasa_schema.dump(z[0]))

        final = {
            "id": x[0].id,
            "po_code": x[0].po_code,
            "po_date": PoSchema(only=["po_date"]).dump(x[0])["po_date"],
            "preq_id": {
                "id": x[1].id,
                "req_code": x[1].req_code,
                "req_date": PreqSchema(only=["req_date"]).dump(x[1])["req_date"],
                "req_dep": ccost_schema.dump(x[2]),
                "req_ket": x[1].req_ket,
                "status": x[1].status,
            },
            "ppn_type": x[0].ppn_type,
            "sup_id": supplier_schema.dump(x[3]),
            "ref_sup": x[0].ppn_type,
            "top": rpay_schema.dump(x[4]),
            "due_date": PoSchema(only=["due_date"]).dump(x[0])["due_date"],
            "split_inv": x[0].split_inv,
            "prod_disc": x[0].prod_disc,
            "jasa_disc": x[0].jasa_disc,
            "total_disc": x[0].total_disc,
            "status": x[0].status,
            "apprv": x[0].apprv,
            "print": x[0].print,
            "pprod": product,
            "pjasa": jasa,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/so", methods=["POST", "GET"])
@token_required
def so(self):
    if request.method == "POST":
        try:
            so_code = request.json["so_code"]
            so_date = request.json["so_date"]
            pel_id = request.json["pel_id"]
            ppn_type = request.json["ppn_type"]
            sub_addr = request.json["sub_addr"]
            sub_id = request.json["sub_id"]
            req_date = request.json["req_date"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            sprod = request.json["sprod"]
            sjasa = request.json["sjasa"]

            so = SordHdb(
                so_code,
                so_date,
                pel_id,
                ppn_type,
                sub_addr,
                sub_id,
                req_date,
                top,
                due_date,
                split_inv,
                prod_disc,
                jasa_disc,
                total_disc,
                0,
                0,
            )

            db.session.add(so)
            db.session.commit()

            new_prod = []
            remain = 0
            for x in sprod:
                if x["prod_id"] and x["unit_id"] and x["order"]:
                    new_prod.append(
                        SprodDdb(
                            so.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["location"],
                            x["request"],
                            x["order"],
                            None,
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in sjasa:
                if x["sup_id"] and x["jasa_id"] and x["unit_id"] and x["qty"]:
                    new_jasa.append(
                        SjasaDdb(
                            so.id,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["qty"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            result = response(200, "Berhasil", True, sord_schema.dump(so))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        so = (
            db.session.query(SordHdb, RulesPayMdb)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == SordHdb.top)
            .order_by(SordHdb.id.asc())
            .all()
        )

        cust = CustomerMdb.query.all()

        sprod = (
            db.session.query(SprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == SprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == SprodDdb.unit_id)
            .all()
        )

        sjasa = (
            db.session.query(SjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == SjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == SjasaDdb.unit_id)
            .all()
        )

        final = []
        for x in so:
            product = []
            for y in sprod:
                if y[0].so_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    product.append(sprod_schema.dump(y[0]))

            jasa = []
            for z in sjasa:
                if z[0].so_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(sjasa_schema.dump(z[0]))

            for a in cust:
                if a.id == x[0].pel_id:
                    x[0].pel_id = customer_schema.dump(a)

            if x[0].sub_addr:
                for b in cust:
                    if b.id == x[0].sub_id:
                        x[0].sub_id = customer_schema.dump(b)

            final.append(
                {
                    "id": x[0].id,
                    "so_code": x[0].so_code,
                    "so_date": SordSchema(only=["so_date"]).dump(x[0])["so_date"],
                    "pel_id": x[0].pel_id,
                    "ppn_type": x[0].ppn_type,
                    "sub_addr": x[0].sub_addr,
                    "sub_id": x[0].sub_id,
                    "req_date": SordSchema(only=["req_date"]).dump(x[0])["req_date"],
                    "top": rpay_schema.dump(x[1]),
                    "due_date": SordSchema(only=["due_date"]).dump(x[0])["due_date"],
                    "split_inv": x[0].split_inv,
                    "prod_disc": x[0].prod_disc,
                    "jasa_disc": x[0].jasa_disc,
                    "total_disc": x[0].total_disc,
                    "status": x[0].status,
                    "print": x[0].print,
                    "sprod": product,
                    "sjasa": jasa,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/so/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def so_id(self, id):
    so = SordHdb.query.filter(SordHdb.id == id).first()
    if request.method == "PUT":
        try:
            so_code = request.json["so_code"]
            so_date = request.json["so_date"]
            pel_id = request.json["pel_id"]
            ppn_type = request.json["ppn_type"]
            sub_addr = request.json["sub_addr"]
            sub_id = request.json["sub_id"]
            req_date = request.json["req_date"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            sprod = request.json["sprod"]
            sjasa = request.json["sjasa"]

            so.so_code = so_code
            so.so_date = so_date
            so.pel_id = pel_id
            so.ppn_type = ppn_type
            so.sub_addr = sub_addr
            so.sub_id = sub_id
            so.req_date = req_date
            so.top = top
            so.due_date = due_date
            so.split_inv = split_inv
            so.prod_disc = prod_disc
            so.jasa_disc = jasa_disc
            so.total_disc = total_disc

            product = SprodDdb.query.filter(SprodDdb.so_id == so.id)
            jasa = SjasaDdb.query.filter(SjasaDdb.so_id == so.id)

            new_prod = []
            for x in sprod:
                for y in product:
                    if x["id"] == y.id:
                        y.prod_id = x["prod_id"]
                        y.unit_id = x["unit_id"]
                        y.location = x["location"]
                        y.request = x["request"]
                        y.order = x["order"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.nett_price = x["nett_price"]
                        y.total = x["total"]
                if x["id"] == 0 and x["prod_id"] and x["unit_id"] and x["order"]:
                    new_prod.append(
                        SprodDdb(
                            so.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["location"],
                            x["request"],
                            x["order"],
                            None,
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in sjasa:
                for y in jasa:
                    if x["id"] == y.id:
                        y.sup_id = x["sup_id"]
                        y.jasa_id = x["jasa_id"]
                        y.unit_id = x["unit_id"]
                        y.qty = x["qty"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.total = x["total"]
                if (
                    x["id"] == 0
                    and x["sup_id"]
                    and x["jasa_id"]
                    and x["unit_id"]
                    and x["qty"]
                ):
                    new_jasa.append(
                        SjasaDdb(
                            so.id,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["qty"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            result = response(200, "Berhasil", True, sord_schema.dump(so))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        product = SprodDdb.query.filter(SprodDdb.so_id == so.id)
        jasa = SjasaDdb.query.filter(SjasaDdb.so_id == so.id)

        for x in product:
            db.session.delete(x)

        for x in jasa:
            db.session.delete(x)

        db.session.delete(so)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        x = (
            db.session.query(SordHdb, RulesPayMdb)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == SordHdb.top)
            .filter(SordHdb.id == id)
            .order_by(SordHdb.id.asc())
            .first()
        )

        cust = CustomerMdb.query.all()

        sprod = (
            db.session.query(SprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == SprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == SprodDdb.unit_id)
            .all()
        )

        sjasa = (
            db.session.query(SjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == SjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == SjasaDdb.unit_id)
            .all()
        )

        product = []
        for y in sprod:
            if y[0].so_id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                product.append(sprod_schema.dump(y[0]))

        jasa = []
        for z in sjasa:
            if z[0].so_id == x[0].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(sjasa_schema.dump(z[0]))

        for a in cust:
            if a.id == x[0].pel_id:
                x[0].pel_id = customer_schema.dump(a)

        if x[0].sub_addr:
            for b in cust:
                if b.id == x[0].sub_id:
                    x[0].sub_id = customer_schema.dump(b)

        final = {
            "id": x[0].id,
            "so_code": x[0].so_code,
            "so_date": SordSchema(only=["so_date"]).dump(x[0])["so_date"],
            "pel_id": x[0].pel_id,
            "ppn_type": x[0].ppn_type,
            "sub_addr": x[0].sub_addr,
            "sub_id": x[0].sub_id,
            "req_date": SordSchema(only=["req_date"]).dump(x[0])["req_date"],
            "top": rpay_schema.dump(x[1]),
            "due_date": SordSchema(only=["due_date"]).dump(x[0])["due_date"],
            "split_inv": x[0].split_inv,
            "prod_disc": x[0].prod_disc,
            "jasa_disc": x[0].jasa_disc,
            "total_disc": x[0].total_disc,
            "status": x[0].status,
            "print": x[0].print,
            "sprod": product,
            "sjasa": jasa,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/order", methods=["POST", "GET"])
@token_required
def order(self):
    if request.method == "POST":
        try:
            ord_code = request.json["ord_code"]
            ord_date = request.json["ord_date"]
            faktur = request.json["faktur"]
            po_id = request.json["po_id"]
            dep_id = request.json["dep_id"]
            sup_id = request.json["sup_id"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            dprod = request.json["dprod"]
            djasa = request.json["djasa"]

            do = OrdpbHdb(
                ord_code,
                ord_date,
                faktur,
                po_id,
                dep_id,
                sup_id,
                top,
                due_date,
                split_inv,
                prod_disc,
                jasa_disc,
                total_disc,
                0,
                0,
            )

            db.session.add(do)
            db.session.commit()

            new_product = []
            for x in dprod:
                if x["prod_id"] and x["unit_id"] and x["order"]:
                    new_product.append(
                        DprodDdb(
                            do.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["location"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in djasa:
                if x["jasa_id"] and x["sup_id"] and x["unit_id"] and x["order"]:
                    new_jasa.append(
                        DjasaDdb(
                            do.id,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            if len(new_product) > 0:
                db.session.add_all(new_product)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            if po_id:
                po = PoMdb.query.filter(PoMdb.id == po_id).first()
                po.status = 1
                db.session.commit()

            if faktur:
                faktur = FkpbHdb(ord_code, ord_date, do.id, None, None, None)

                db.session.add(faktur)

                db.session.commit()

                UpdatePembelian(faktur.id, self.id, False)

            UpdateStock(do.id, False)

            result = response(200, "Berhasil", True, dord_schema.dump(do))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        do = (
            db.session.query(OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb)
            .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
            .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
            .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
            .all()
        )

        dprod = (
            db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
            .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
            .all()
        )

        djasa = (
            db.session.query(DjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
            .all()
        )

        final = []
        for x in do:
            product = []
            for y in dprod:
                if y[0].ord_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    y[0].location = loct_schema.dump(y[3]) if y[0].location else None
                    product.append(dprod_schema.dump(y[0]))

            jasa = []
            for z in djasa:
                if z[0].ord_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(djasa_schema.dump(z[0]))

            final.append(
                {
                    "id": x[0].id,
                    "ord_code": x[0].ord_code,
                    "ord_date": DordSchema(only=["ord_date"]).dump(x[0])["ord_date"],
                    "faktur": x[0].faktur,
                    "po_id": po_schema.dump(x[4]),
                    "dep_id": ccost_schema.dump(x[1]),
                    "sup_id": supplier_schema.dump(x[2]),
                    "top": rpay_schema.dump(x[3]),
                    "due_date": DordSchema(only=["due_date"]).dump(x[0])["due_date"],
                    "split_inv": x[0].split_inv,
                    "prod_disc": x[0].prod_disc,
                    "jasa_disc": x[0].jasa_disc,
                    "total_disc": x[0].total_disc,
                    "status": x[0].status,
                    "print": x[0].print,
                    "dprod": product,
                    "djasa": jasa,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/order/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def ord_id(self, id):
    do = OrdpbHdb.query.filter(OrdpbHdb.id == id).first()
    if request.method == "PUT":
        try:
            ord_code = request.json["ord_code"]
            ord_date = request.json["ord_date"]
            faktur = request.json["faktur"]
            dep_id = request.json["dep_id"]
            sup_id = request.json["sup_id"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            dprod = request.json["dprod"]
            djasa = request.json["djasa"]

            do.ord_code = ord_code
            do.ord_date = ord_date
            do.faktur = faktur
            do.dep_id = dep_id
            do.sup_id = sup_id
            do.top = top
            do.due_date = due_date
            do.split_inv = split_inv
            do.prod_disc = prod_disc
            do.jasa_disc = jasa_disc
            do.total_disc = total_disc

            product = DprodDdb.query.filter(DprodDdb.ord_id == do.id)
            jasa = DjasaDdb.query.filter(DjasaDdb.ord_id == do.id)

            new_prod = []
            for x in dprod:
                for y in product:
                    if x["id"] == y.id:
                        y.prod_id = x["prod_id"]
                        y.unit_id = x["unit_id"]
                        y.order = x["order"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.nett_price = x["nett_price"]
                        y.total = x["total"]
                        y.location = x["location"]
                if x["id"] == 0 and x["prod_id"] and x["unit_id"] and x["order"]:
                    new_prod.append(
                        DprodDdb(
                            do.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["location"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in djasa:
                for y in jasa:
                    if x["id"] == y.id:
                        y.sup_id = x["sup_id"]
                        y.jasa_id = x["jasa_id"]
                        y.unit_id = x["unit_id"]
                        y.order = x["order"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.total = x["total"]
                if (
                    x["id"] == 0
                    and x["sup_id"]
                    and x["jasa_id"]
                    and x["unit_id"]
                    and x["order"]
                ):
                    new_jasa.append(
                        DjasaDdb(
                            do.id,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            result = response(200, "Berhasil", True, dord_schema.dump(do))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        po = PoMdb.query.filter(PoMdb.id == do.po_id).first()
        if po:
            po.status = 0
            db.session.commit()
        UpdateStock(do.id, True)
        product = DprodDdb.query.filter(DprodDdb.ord_id == do.id)
        jasa = DjasaDdb.query.filter(DjasaDdb.ord_id == do.id)

        for x in product:
            db.session.delete(x)

        for x in jasa:
            db.session.delete(x)

        db.session.delete(do)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        x = (
            db.session.query(OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb)
            .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
            .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
            .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
            .filter(OrdpbHdb.id == id)
            .first()
        )

        dprod = (
            db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
            .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
            .all()
        )

        djasa = (
            db.session.query(DjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
            .all()
        )

        product = []
        for y in dprod:
            if y[0].ord_id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                y[0].lcoation = unit_schema.dump(y[3]) if y[0].location else None
                product.append(dprod_schema.dump(y[0]))

        jasa = []
        for z in djasa:
            if z[0].ord_id == x[0].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(djasa_schema.dump(z[0]))

        final = {
            "id": x[0].id,
            "ord_code": x[0].ord_code,
            "ord_date": DordSchema(only=["ord_date"]).dump(x[0])["ord_date"],
            "faktur": x[0].faktur,
            "po_id": po_schema.dump(x[4]),
            "dep_id": ccost_schema.dump(x[1]),
            "sup_id": supplier_schema.dump(x[2]),
            "top": rpay_schema.dump(x[3]),
            "due_date": DordSchema(only=["due_date"]).dump(x[0])["due_date"],
            "split_inv": x[0].split_inv,
            "prod_disc": x[0].prod_disc,
            "jasa_disc": x[0].jasa_disc,
            "total_disc": x[0].total_disc,
            "status": x[0].status,
            "print": x[0].print,
            "dprod": product,
            "djasa": jasa,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/order/date", methods=["POST"])
@token_required
def order_date(self):
    start_date = request.json["start_date"]
    end_date = request.json["end_date"]

    do = (
        db.session.query(OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb)
        .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
        .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
        .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
        .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
        .filter(OrdpbHdb.ord_date >= start_date, OrdpbHdb.ord_date <= end_date)
        .all()
    )

    dprod = (
        db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
        .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
        .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
        .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
        .all()
    )

    djasa = (
        db.session.query(DjasaDdb, JasaMdb, UnitMdb)
        .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
        .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
        .all()
    )

    final = []
    for x in do:
        product = []
        for y in dprod:
            if y[0].ord_id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                y[0].location = loct_schema.dump(y[3]) if y[0].location else None
                product.append(dprod_schema.dump(y[0]))

        jasa = []
        for z in djasa:
            if z[0].ord_id == x[0].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(djasa_schema.dump(z[0]))

        final.append(
            {
                "id": x[0].id,
                "ord_code": x[0].ord_code,
                "ord_date": DordSchema(only=["ord_date"]).dump(x[0])["ord_date"],
                "faktur": x[0].faktur,
                "po_id": po_schema.dump(x[4]),
                "dep_id": ccost_schema.dump(x[1]),
                "sup_id": supplier_schema.dump(x[2]),
                "top": rpay_schema.dump(x[3]),
                "due_date": DordSchema(only=["due_date"]).dump(x[0])["due_date"],
                "split_inv": x[0].split_inv,
                "prod_disc": x[0].prod_disc,
                "jasa_disc": x[0].jasa_disc,
                "total_disc": x[0].total_disc,
                "status": x[0].status,
                "print": x[0].print,
                "dprod": product,
                "djasa": jasa,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/faktur/code", methods=["POST", "GET"])
@token_required
def faktur_code(self):
    now = datetime.now().strftime("%d%m%y")
    fk = "FK/" + now + "/" + str(round(time.time() * 10000))[-6:]
    return response(200, "success", True, fk)


@app.route("/v1/api/faktur", methods=["POST", "GET"])
@token_required
def faktur(self):
    if request.method == "POST":
        fk_code = request.json["fk_code"]
        fk_date = request.json["fk_date"]
        ord_id = request.json["ord_id"]
        fk_tax = request.json["fk_tax"]
        fk_ppn = request.json["fk_ppn"]
        fk_desc = request.json["fk_desc"]

        faktur = FkpbHdb(fk_code, fk_date, ord_id, fk_tax, fk_ppn, fk_desc)

        db.session.add(faktur)

        db.session.commit()

        UpdatePembelian(faktur.id, self.id, False)

        return response(200, "success", True, fkpb_schema.dump(faktur))
    else:
        fk = (
            db.session.query(FkpbHdb, OrdpbHdb)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
            .all()
        )
        dprod = (
            db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
            .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
            .all()
        )

        djasa = (
            db.session.query(DjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
            .all()
        )

        final = []
        for x in fk:
            product = []
            if x[1]:
                for y in dprod:
                    if x[1]:
                        if y[0].ord_id == x[1].id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].location = (
                                loct_schema.dump(y[3]) if y[0].location else None
                            )
                            product.append(dprod_schema.dump(y[0]))

            jasa = []
            if x[1]:
                for z in djasa:
                    if x[1]:
                        if z[0].ord_id == x[1].id:
                            z[0].jasa_id = jasa_schema.dump(z[1])
                            z[0].unit_id = unit_schema.dump(z[2])
                            jasa.append(djasa_schema.dump(z[0]))

            final.append(
                {
                    "id": x[0].id,
                    "fk_code": x[0].fk_code,
                    "fk_date": FkpbSchema(only=["fk_date"]).dump(x[0])["fk_date"]
                    if x[0].fk_date
                    else None,
                    "fk_tax": x[0].fk_tax,
                    "fk_ppn": x[0].fk_ppn,
                    "fk_lunas": x[0].fk_lunas,
                    "fk_desc": x[0].fk_desc,
                    "ord_id": dord_schema.dump(x[1]),
                    "product": product,
                    "jasa": jasa,
                }
            )

        return response(200, "success", True, final)


@app.route("/v1/api/faktur/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def faktur_id(self, id):
    fk = FkpbHdb.query.filter(FkpbHdb.id == id).first()
    if request.method == "PUT":
        fk_date = request.json["fk_date"]
        ord_id = request.json["ord_id"]
        fk_tax = request.json["fk_tax"]
        fk_ppn = request.json["fk_ppn"]
        fk_desc = request.json["fk_desc"]

        fk.fk_date = fk_date
        fk.ord_id = ord_id
        fk.fk_tax = fk_tax
        fk.fk_ppn = fk_ppn
        fk.fk_desc = fk_desc

        db.session.commit()

        return response(200, "success", True, fkpb_schema.dump(fk))
    elif request.method == "DELETE":
        UpdatePembelian(fk.id, self.id, True)
        prod = DprodDdb.query.filter(DprodDdb.ord_id == fk.ord_id).all()

        for x in prod:
            x.location = None

        db.session.delete(fk)
        db.session.commit()

        return response(200, "success", True, None)
    else:
        x = (
            db.session.query(FkpbHdb, OrdpbHdb)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
            .filter(FkpbHdb.id == id)
            .first()
        )
        dprod = (
            db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
            .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
            .all()
        )

        djasa = (
            db.session.query(DjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
            .all()
        )

        product = []
        for y in dprod:
            if y[0].ord_id == x[1].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                y[0].location = loct_schema.dump(y[3]) if y[0].location else None
                product.append(dprod_schema.dump(y[0]))

        jasa = []
        for z in djasa:
            if z[0].ord_id == x[1].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(djasa_schema.dump(z[0]))

        final = {
            "fk_code": x[0].fk_code,
            "fk_date": FkpbSchema(only=["fk_date"]).dump(x[0])["fk_date"]
            if x[0].fk_date
            else None,
            "fk_tax": x[0].fk_tax,
            "fk_ppn": x[0].fk_ppn,
            "fk_lunas": x[0].fk_lunas,
            "fk_desc": x[0].fk_desc,
            "ord_id": dord_schema.dump(x[1]),
            "product": product,
            "jasa": jasa,
        }

        return response(200, "success", True, final)


@app.route("/v1/api/retur-order", methods=["POST", "GET"])
@token_required
def retur_order(self):
    if request.method == "POST":
        try:
            ret_code = request.json["ret_code"]
            ret_date = request.json["ret_date"]
            fk_id = request.json["fk_id"]
            product = request.json["product"]

            retur = RetordHdb(ret_code, ret_date, fk_id)

            db.session.add(retur)
            db.session.commit()

            new_prod = []
            for x in product:
                if x["prod_id"] and x["unit_id"] and x["retur"] and int(x["retur"]) > 0:
                    new_prod.append(
                        ReprodDdb(
                            retur.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["retur"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            db.session.add_all(new_prod)
            db.session.commit()

            result = response(200, "success", True, retord_schema.dump(retur))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        retur = (
            db.session.query(RetordHdb, FkpbHdb, OrdpbHdb)
            .outerjoin(FkpbHdb, FkpbHdb.id == RetordHdb.fk_id)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
            .all()
        )

        product = (
            db.session.query(ReprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
            .all()
        )

        result = []
        for x in retur:
            prod = []
            for y in product:
                if x[0].id == y[0].ret_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    prod.append(reprod_schema.dump(y[0]))

            if x[1]:
                x[1].ord_id = dord_schema.dump(x[2])
            result.append(
                {
                    "id": x[0].id,
                    "ret_code": x[0].ret_code,
                    "ret_date": RetordSchema(only=["ret_date"]).dump(x[0])["ret_date"]
                    if x[0].ret_date
                    else None,
                    "fk_id": fkpb_schema.dump(x[1]),
                    "product": prod,
                }
            )

        return response(200, "success", True, result)


@app.route("/v1/api/retur-order/<int:id>", methods=["PUT", "DELETE", "GET"])
@token_required
def retur_order_id(self, id):
    ret = RetordHdb.query.filter(RetordHdb.id == id).first()
    if request.method == "PUT":
        try:
            ret_code = request.json["ret_code"]
            ret_date = request.json["ret_date"]
            fk_id = request.json["fk_id"]
            product = request.json["product"]

            ret.ret_code = ret_code
            ret.ret_date = ret_date
            ret.fk_id = fk_id

            # product = ReprodDdb.query.filter(ReprodDdb.id == ret.id)

            new_prod = []
            for x in product:
                for y in product:
                    if x["id"] == y.id:
                        y.prod_id = x["prod_id"]
                        y.unit_id = x["unit_id"]
                        y.retur = x["retur"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.nett_price = x["nett_price"]
                        y.total = x["total"]
                if x["id"] == 0 and x["prod_id"] and x["unit_id"] and x["retur"]:
                    new_prod.append(
                        ReprodDdb(
                            ret.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["retur"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            db.session.commit()

            result = response(200, "Berhasil", True, retord_schema.dump(ret))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        db.session.delete(ret)
        db.session.commit()

        return response(200, "success", True, None)

    else:
        x = (
            db.session.query(RetordHdb, FkpbHdb, OrdpbHdb)
            .outerjoin(FkpbHdb, FkpbHdb.id == RetordHdb.fk_id)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
            .filter(RetordHdb.id == id)
            .first()
        )

        product = (
            db.session.query(ReprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
            .all()
        )

        product = []
        for y in product:
            if y[0].id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                product.append(reprod_schema.dump(y[0]))

        final = {
            "id": x[0].id,
            "ret_code": x[0].ret_code,
            "ret_date": RetSaleSchema(only=["ret_date"]).dump(x[0])["ret_date"],
            "fk_id": fkpb_schema.dump(x[2]) if x[2] else None,
            "product": product,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/retur-sales", methods=["POST", "GET"])
@token_required
def retur_sales(self):
    if request.method == "POST":
        try:
            ret_code = request.json["ret_code"]
            ret_date = request.json["ret_date"]
            sale_id = request.json["sale_id"]
            product = request.json["product"]

            retur = RetSaleHdb(ret_code, ret_date, sale_id)

            db.session.add(retur)
            db.session.commit()

            new_prod = []
            for x in product:
                if x["prod_id"] and x["unit_id"] and x["retur"] and int(x["retur"]) > 0:
                    new_prod.append(
                        ReprodDdb(
                            retur.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["retur"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            db.session.add_all(new_prod)
            db.session.commit()

            result = response(200, "success", True, retsale_schema.dump(retur))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        retur = (
            db.session.query(RetSaleHdb, OrdpjHdb, SordHdb)
            .outerjoin(OrdpjHdb, OrdpjHdb.id == RetSaleHdb.sale_id)
            .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
            .all()
        )

        product = (
            db.session.query(ReprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
            .all()
        )

        result = []
        for x in retur:
            prod = []
            for y in product:
                if x[0].id == y[0].ret_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    prod.append(reprod_schema.dump(y[0]))

            if x[1]:
                x[1].so_id = sord_schema.dump(x[2])
            result.append(
                {
                    "id": x[0].id,
                    "ret_code": x[0].ret_code,
                    "ret_date": RetSaleSchema(only=["ret_date"]).dump(x[0])["ret_date"]
                    if x[0].ret_date
                    else None,
                    "sale_id": ordpj_schema.dump(x[1]),
                    "product": prod,
                }
            )

        return response(200, "success", True, result)


@app.route("/v1/api/retur-sales/<int:id>", methods=["PUT", "DELETE", "GET"])
@token_required
def retur_sale_id(self, id):
    ret = RetSaleHdb.query.filter(RetSaleHdb.id == id).first()
    if request.method == "PUT":
        try:
            ret_code = request.json["ret_code"]
            ret_date = request.json["ret_date"]
            sale_id = request.json["sale_id"]
            product = request.json["product"]

            ret.ret_code = ret_code
            ret.ret_date = ret_date
            ret.sale_id = sale_id

            # product = ReprodDdb.query.filter(ReprodDdb.id == ret.id)

            new_prod = []
            for x in product:
                for y in product:
                    if x["id"] == y.id:
                        y.prod_id = x["prod_id"]
                        y.unit_id = x["unit_id"]
                        y.retur = x["retur"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.nett_price = x["nett_price"]
                        y.total = x["total"]
                if x["id"] == 0 and x["prod_id"] and x["unit_id"] and x["retur"]:
                    new_prod.append(
                        ReprodDdb(
                            ret.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["retur"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            db.session.commit()

            result = response(200, "Berhasil", True, retsale_schema.dump(ret))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        db.session.delete(ret)
        db.session.commit()

        return response(200, "success", True, None)

    else:
        x = (
            db.session.query(RetSaleHdb, OrdpjHdb, SordHdb)
            .outerjoin(OrdpjHdb, OrdpjHdb.id == RetSaleHdb.sale_id)
            .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
            .filter(RetSaleHdb.id == id)
            .first()
        )

        product = (
            db.session.query(ReprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == ReprodDdb.unit_id)
            .all()
        )

        product = []
        for y in product:
            if y[0].id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                product.append(reprod_schema.dump(y[0]))

        final = {
            "id": x[0].id,
            "ret_code": x[0].ret_code,
            "ret_date": RetSaleSchema(only=["ret_date"]).dump(x[0])["ret_date"],
            "sale_id": ordpj_schema.dump(x[2]) if x[2] else None,
            "product": product,
        }

        return response(200, "Berhasil", True, final)


# @app.route("/v1/api/faktur/<int:id>", methods=["PUT", "GET", 'DELETE'])
# @token_required
# def faktur_id(self, id):
#
#     if request.method == 'PUT':
#
#     elif request.method == 'DELETE':
#
#     else:


@app.route("/v1/api/sales", methods=["POST", "GET"])
@token_required
def sls(self):
    if request.method == "POST":
        try:
            ord_code = request.json["ord_code"]
            ord_date = request.json["ord_date"]
            so_id = request.json["so_id"]
            invoice = request.json["invoice"]
            pel_id = request.json["pel_id"]
            ppn_type = request.json["ppn_type"]
            sub_addr = request.json["sub_addr"]
            sub_id = request.json["sub_id"]
            slsm_id = request.json["slsm_id"]
            req_date = request.json["req_date"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            jprod = request.json["jprod"]
            jjasa = request.json["jjasa"]

            sls = OrdpjHdb(
                ord_code,
                ord_date,
                so_id,
                invoice,
                pel_id,
                ppn_type,
                sub_addr,
                sub_id,
                slsm_id,
                req_date,
                top,
                due_date,
                split_inv,
                prod_disc,
                jasa_disc,
                total_disc,
                0,
                0,
            )

            db.session.add(sls)
            db.session.commit()

            new_product = []
            for x in jprod:
                if x["prod_id"] and x["unit_id"] and x["order"]:
                    new_product.append(
                        JprodDdb(
                            sls.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["location"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in jjasa:
                if x["jasa_id"] and x["sup_id"] and x["unit_id"] and x["order"]:
                    new_jasa.append(
                        JjasaDdb(
                            sls.id,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            if len(new_product) > 0:
                db.session.add_all(new_product)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            UpdateAr(False, sls.id, self.id)

            result = response(200, "Berhasil", True, ordpj_schema.dump(sls))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        sls = (
            db.session.query(OrdpjHdb, RulesPayMdb, SordHdb, SalesMdb)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpjHdb.top)
            .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
            .outerjoin(SalesMdb, SalesMdb.id == OrdpjHdb.slsm_id)
            .all()
        )

        cust = CustomerMdb.query.all()

        jprod = (
            db.session.query(JprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == JprodDdb.unit_id)
            .all()
        )

        jjasa = (
            db.session.query(JjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == JjasaDdb.unit_id)
            .all()
        )

        final = []
        for x in sls:
            product = []
            for y in jprod:
                if y[0].pj_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    product.append(jprod_schema.dump(y[0]))

            jasa = []
            for z in jjasa:
                if z[0].pj_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(jjasa_schema.dump(z[0]))

            for a in cust:
                if a.id == x[0].pel_id:
                    x[0].pel_id = customer_schema.dump(a)

            if x[0].sub_addr:
                for b in cust:
                    if b.id == x[0].sub_id:
                        x[0].sub_id = customer_schema.dump(b)

            final.append(
                {
                    "id": x[0].id,
                    "ord_code": x[0].ord_code,
                    "ord_date": OrdpjSchema(only=["ord_date"]).dump(x[0])["ord_date"],
                    "so_id": sord_schema.dump(x[2]) if x[2] else None,
                    "invoice": x[0].invoice,
                    "pel_id": x[0].pel_id,
                    "ppn_type": x[0].ppn_type,
                    "sub_addr": x[0].sub_addr,
                    "sub_id": x[0].sub_id,
                    "slsm_id": sales_schema.dump(x[3]) if x[3] else None,
                    "req_date": OrdpjSchema(only=["req_date"]).dump(x[0])["req_date"],
                    "top": rpay_schema.dump(x[1]) if x[1] else None,
                    "due_date": OrdpjSchema(only=["due_date"]).dump(x[0])["due_date"],
                    "split_inv": x[0].split_inv,
                    "prod_disc": x[0].prod_disc,
                    "jasa_disc": x[0].jasa_disc,
                    "total_disc": x[0].total_disc,
                    "status": x[0].status,
                    "print": x[0].print,
                    "jprod": product,
                    "jjasa": jasa,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/sales/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def sls_id(self, id):
    sls = OrdpjHdb.query.filter(OrdpjHdb.id == id).first()
    if request.method == "PUT":
        try:
            ord_code = request.json["ord_code"]
            ord_date = request.json["ord_date"]
            so_id = request.json["so_id"]
            invoice = request.json["invoice"]
            pel_id = request.json["pel_id"]
            ppn_type = request.json["ppn_type"]
            sub_addr = request.json["sub_addr"]
            sub_id = request.json["sub_id"]
            slsm_id = request.json["slsm_id"]
            req_date = request.json["req_date"]
            top = request.json["top"]
            due_date = request.json["due_date"]
            split_inv = request.json["split_inv"]
            prod_disc = request.json["prod_disc"]
            jasa_disc = request.json["jasa_disc"]
            total_disc = request.json["total_disc"]
            jprod = request.json["jprod"]
            jjasa = request.json["jjasa"]

            sls.ord_code = ord_code
            sls.ord_date = ord_date
            sls.so_id = so_id
            sls.invoice = invoice
            sls.pel_id = pel_id
            sls.ppn_type = ppn_type
            sls.sub_addr = sub_addr
            sls.sub_id = sub_id
            sls.slsm_id = slsm_id
            sls.req_date = req_date
            sls.top = top
            sls.due_date = due_date
            sls.split_inv = split_inv
            sls.prod_disc = prod_disc
            sls.jasa_disc = jasa_disc
            sls.total_disc = total_disc

            product = JprodDdb.query.filter(JprodDdb.pj_id == sls.id)
            jasa = JjasaDdb.query.filter(JjasaDdb.pj_id == sls.id)

            new_prod = []
            for x in jprod:
                for y in product:
                    if x["id"] == y.id:
                        y.prod_id = x["prod_id"]
                        y.unit_id = x["unit_id"]
                        y.order = x["order"]
                        y.location = x["location"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.nett_price = x["nett_price"]
                        y.total = x["total"]
                if x["id"] == 0 and x["prod_id"] and x["unit_id"] and x["order"]:
                    new_prod.append(
                        JprodDdb(
                            sls.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["location"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["nett_price"],
                            x["total"],
                        )
                    )

            new_jasa = []
            for x in jjasa:
                for y in jasa:
                    if x["id"] == y.id:
                        y.sup_id = x["sup_id"]
                        y.jasa_id = x["jasa_id"]
                        y.unit_id = x["unit_id"]
                        y.order = x["order"]
                        y.price = x["price"]
                        y.disc = x["disc"]
                        y.total = x["total"]
                if (
                    x["id"] == 0
                    and x["sup_id"]
                    and x["jasa_id"]
                    and x["unit_id"]
                    and x["order"]
                ):
                    new_jasa.append(
                        JjasaDdb(
                            sls.id,
                            x["sup_id"],
                            x["jasa_id"],
                            x["unit_id"],
                            x["order"],
                            x["price"],
                            x["disc"],
                            x["total"],
                        )
                    )

            if len(new_prod) > 0:
                db.session.add_all(new_prod)

            if len(new_jasa) > 0:
                db.session.add_all(new_jasa)

            db.session.commit()

            result = response(200, "Berhasil", True, ordpj_schema.dump(sls))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        UpdateAr(True, sls.id, self.id)
        product = JprodDdb.query.filter(JprodDdb.pj_id == sls.id)
        jasa = JprodDdb.query.filter(JprodDdb.pj_id == sls.id)

        for x in product:
            db.session.delete(x)

        for x in jasa:
            db.session.delete(x)

        db.session.delete(sls)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        x = (
            db.session.query(OrdpjHdb, RulesPayMdb, SordHdb, SalesMdb)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpjHdb.top)
            .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
            .outerjoin(SalesMdb, SalesMdb.id == OrdpjHdb.slsm_id)
            .filter(OrdpjHdb.id == id)
            .order_by(OrdpbHdb.id.asc())
            .first()
        )

        cust = CustomerMdb.query.all()

        jprod = (
            db.session.query(JprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == JprodDdb.unit_id)
            .all()
        )

        jjasa = (
            db.session.query(JjasaDdb, JasaMdb, UnitMdb)
            .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
            .outerjoin(UnitMdb, UnitMdb.id == JjasaDdb.unit_id)
            .all()
        )

        product = []
        for y in jprod:
            if y[0].pj_id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                product.append(jprod_schema.dump(y[0]))

        jasa = []
        for z in jjasa:
            if z[0].pj_id == x[0].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(jjasa_schema.dump(z[0]))

        for a in cust:
            if a.id == x[0].pel_id:
                x[0].pel_id = customer_schema.dump(a)

        if x[0].sub_addr:
            for b in cust:
                if b.id == x[0].sub_id:
                    x[0].sub_id = customer_schema.dump(b)

        final = {
            "id": x[0].id,
            "ord_code": x[0].ord_code,
            "ord_date": OrdpjSchema(only=["ord_date"]).dump(x[0])["ord_date"],
            "so_id": sord_schema.dump(x[2]) if x[2] else None,
            "invoice": x[0].invoice,
            "pel_id": x[0].pel_id,
            "ppn_type": x[0].ppn_type,
            "sub_addr": x[0].sub_addr,
            "sub_id": x[0].sub_id,
            "slsm_id": sales_schema.dump(x[3]) if x[3] else None,
            "req_date": OrdpjSchema(only=["req_date"]).dump(x[0])["req_date"],
            "top": rpay_schema.dump(x[1]) if x[1] else None,
            "due_date": OrdpjSchema(only=["due_date"]).dump(x[0])["due_date"],
            "split_inv": x[0].split_inv,
            "prod_disc": x[0].prod_disc,
            "jasa_disc": x[0].jasa_disc,
            "total_disc": x[0].total_disc,
            "status": x[0].status,
            "print": x[0].print,
            "jprod": product,
            "jjasa": jasa,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/expense", methods=["POST", "GET"])
@token_required
def expense(self):
    if request.method == "POST":
        try:
            exp_code = request.json["exp_code"]
            exp_date = request.json["exp_date"]
            exp_type = request.json["exp_type"]
            exp_dep = request.json["exp_dep"]
            exp_acc = request.json["exp_acc"]
            exp_prj = request.json["exp_prj"]
            acq_sup = request.json["acq_sup"]
            acq_pay = request.json["acq_pay"]
            kas_acc = request.json["kas_acc"]
            bank_acc = request.json["bank_acc"]
            bank_id = request.json["bank_id"]
            bank_ref = request.json["bank_ref"]
            giro_num = request.json["giro_num"]
            giro_date = request.json["giro_date"]
            acq = request.json["acq"]
            exp = request.json["exp"]

            exps = ExpHdb(
                exp_code,
                exp_date,
                exp_type,
                exp_acc,
                exp_dep,
                exp_prj,
                acq_sup,
                acq_pay,
                kas_acc,
                bank_acc,
                bank_id,
                bank_ref,
                giro_num,
                giro_date,
            )

            db.session.add(exps)
            db.session.commit()

            new_exp = []
            for x in exp:
                if x["acc_code"] and x["value"]:
                    new_exp.append(
                        ExpDdb(exps.id, x["acc_code"], x["value"], x["desc"])
                    )

            new_acq = []
            value = 0
            for x in acq:
                if x["fk_id"] and x["value"] and x["payment"] and int(x["payment"]) > 0:
                    value += int(x["payment"])
                    new_acq.append(
                        AcqDdb(exps.id, x["fk_id"], x["value"], x["payment"])
                    )

            if len(new_exp) > 0:
                db.session.add_all(new_exp)

            if len(new_acq) > 0:
                db.session.add_all(new_acq)

            if acq_pay and acq_pay == 3:
                giro = GiroHdb(
                    giro_date, giro_num, bank_id, exps.id, exp_date, acq_sup, value, 0
                )
                db.session.add(giro)
                db.session.commit()
                UpdateApGiro(giro.id)

            db.session.commit()

            if acq_pay and acq_pay != 3:
                UpdateApPayment(exps.id, False)

            result = response(200, "Berhasil", True, exp_schema.dump(exps))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        exps = (
            db.session.query(ExpHdb, BankMdb, SupplierMdb)
            .outerjoin(BankMdb, BankMdb.id == ExpHdb.bank_id)
            .outerjoin(SupplierMdb, SupplierMdb.id == ExpHdb.acq_sup)
            .order_by(ExpHdb.id.desc())
            .all()
        )

        acc = AccouMdb.query.all()

        exp = (
            db.session.query(ExpDdb, AccouMdb)
            .outerjoin(AccouMdb, AccouMdb.id == ExpDdb.acc_code)
            .all()
        )

        acq = (
            db.session.query(AcqDdb, FkpbHdb)
            .outerjoin(FkpbHdb, FkpbHdb.id == AcqDdb.fk_id)
            .all()
        )

        final = []
        for x in exps:
            all_exp = []
            for y in exp:
                if y[0].exp_id == x[0].id:
                    y[0].acc_code = accou_schema.dump(y[1])
                    all_exp.append(dexp_schema.dump(y[0]))

            all_acq = []
            for z in acq:
                if z[0].exp_id == x[0].id:
                    z[0].fk_id = fkpb_schema.dump(z[1])
                    all_acq.append(dacq_schema.dump(z[0]))

            if x[0].exp_acc:
                for a in acc:
                    if a.id == x[0].exp_acc:
                        x[0].exp_acc = accou_schema.dump(a)

            if x[0].kas_acc:
                for b in acc:
                    if b.id == x[0].kas_acc:
                        x[0].kas_acc = accou_schema.dump(b)

            final.append(
                {
                    "id": x[0].id,
                    "exp_code": x[0].exp_code,
                    "exp_date": ExpSchema(only=["exp_date"]).dump(x[0])["exp_date"],
                    "exp_type": x[0].exp_type,
                    "exp_acc": x[0].exp_acc,
                    "exp_dep": x[0].exp_dep,
                    "exp_prj": x[0].exp_prj,
                    "acq_sup": supplier_schema.dump(x[2]) if x[2] else None,
                    "acq_pay": x[0].acq_pay,
                    "kas_acc": x[0].kas_acc,
                    "bank_acc": x[0].bank_acc,
                    "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                    "bank_ref": x[0].bank_ref,
                    "giro_num": x[0].giro_num,
                    "giro_date": ExpSchema(only=["giro_date"]).dump(x[0])["giro_date"],
                    "exp": all_exp,
                    "acq": all_acq,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/expense/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def expense_id(self, id):
    exps = ExpHdb.query.filter(ExpHdb.id == id).first()
    if request.method == "PUT":
        try:
            exp_code = request.json["exp_code"]
            exp_date = request.json["exp_date"]
            exp_type = request.json["exp_type"]
            exp_acc = request.json["exp_acc"]
            exp_dep = request.json["exp_dep"]
            exp_prj = request.json["exp_prj"]
            acq_sup = request.json["acq_sup"]
            acq_pay = request.json["acq_pay"]
            kas_acc = request.json["kas_acc"]
            bank_acc = request.json["bank_acc"]
            bank_id = request.json["bank_id"]
            bank_ref = request.json["bank_ref"]
            giro_num = request.json["giro_num"]
            giro_date = request.json["giro_date"]
            acq = request.json["acq"]
            exp = request.json["exp"]

            exps.exp_code = exp_code
            exps.exp_date = exp_date
            exps.exp_type = exp_type
            exps.exp_acc = exp_acc
            exps.exp_dep = exp_dep
            exps.exp_prj = exp_prj
            exps.acq_sup = acq_sup
            exps.acq_pay = acq_pay
            exps.kas_acc = kas_acc
            exps.bank_acc = bank_acc
            exps.bank_id = bank_id
            exps.bank_ref = bank_ref
            exps.giro_num = giro_num
            exps.giro_date = giro_date

            all_exp = ExpHdb.query.filter(ExpDdb.exp_id == exps.id)
            all_acq = AcqDdb.query.filter(AcqDdb.exp_id == exps.id)

            for x in acq:
                for y in all_acq:
                    if x["id"] == y.id:
                        y.value = x["value"]

            for x in exp:
                for y in all_exp:
                    if x["id"] == y.id:
                        y.acc_code = x["acc_code"]
                        y.value = x["value"]
                        y.desc = x["desc"]

            db.session.commit()

            result = response(200, "Berhasil", True, exp_schema.dump(exps))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        UpdateApPayment(exps.id, True)
        DeleteApPayment(exps.id)
        exp = ExpDdb.query.filter(ExpDdb.exp_id == exps.id)
        acq = AcqDdb.query.filter(AcqDdb.exp_id == exps.id)

        for x in exp:
            db.session.delete(x)

        for x in acq:
            db.session.delete(x)

        db.session.delete(exps)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        exps = (
            db.session.query(ExpHdb, BankMdb, SupplierMdb)
            .outerjoin(BankMdb, BankMdb.id == ExpHdb.bank_id)
            .outerjoin(SupplierMdb, SupplierMdb.id == ExpHdb.acq_sup)
            .filter(ExpHdb.id == id)
            .all()
        )

        acc = AccouMdb.query.all()

        exp = (
            db.session.query(ExpDdb, AccouMdb)
            .outerjoin(AccouMdb, AccouMdb.id == ExpDdb.acc_code)
            .all()
        )

        acq = (
            db.session.query(AcqDdb, FkpbHdb)
            .outerjoin(FkpbHdb, FkpbHdb.id == AcqDdb.fk_id)
            .all()
        )

        final = []
        for x in exps:
            all_exp = []
            for y in exp:
                if y[0].exp_id == x[0].id:
                    y[0].acc_code = accou_schema.dump(y[1])
                    all_exp.append(dexp_schema.dump(y[0]))

            all_acq = []
            for z in acq:
                if z[0].exp_id == x[0].id:
                    z[0].fk_id = fkpb_schema.dump(z[1])
                    all_acq.append(dacq_schema.dump(z[0]))

            if x[0].exp_acc:
                for a in acc:
                    if a.id == x[0].exp_acc:
                        x[0].exp_acc = accou_schema.dump(a)

            if x[0].kas_acc:
                for b in acc:
                    if a.id == x[0].kas_acc:
                        x[0].kas_acc = accou_schema.dump(b)

            final.append(
                {
                    "id": x[0].id,
                    "exp_code": x[0].exp_code,
                    "exp_date": ExpSchema(only=["exp_date"]).dump(x[0])["exp_date"],
                    "exp_type": x[0].exp_type,
                    "exp_acc": x[0].exp_acc,
                    "exp_dep": x[0].exp_dep,
                    "exp_prj": x[0].exp_prj,
                    "acq_sup": supplier_schema.dump(x[2]) if x[2] else None,
                    "acq_pay": x[0].acq_pay,
                    "kas_acc": x[0].kas_acc,
                    "bank_acc": x[0].bank_acc,
                    "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                    "bank_ref": x[0].bank_ref,
                    "giro_num": x[0].giro_num,
                    "giro_date": ExpSchema(only=["giro_date"]).dump(x[0])["giro_date"],
                    "exp": all_exp,
                    "acq": all_acq,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/apcard", methods=["GET"])
@token_required
def apcard(self):
    ap = (
        db.session.query(ApCard, AcqDdb, PoMdb, SupplierMdb, FkpbHdb, GiroHdb)
        .outerjoin(AcqDdb, AcqDdb.id == ApCard.acq_id)
        .outerjoin(PoMdb, PoMdb.id == ApCard.po_id)
        .outerjoin(SupplierMdb, SupplierMdb.id == ApCard.sup_id)
        .outerjoin(FkpbHdb, FkpbHdb.ord_id == ApCard.ord_id)
        .outerjoin(GiroHdb, GiroHdb.id == ApCard.giro_id)
        .all()
    )

    final = []
    for x in ap:
        final.append(
            {
                "id": x[0].id,
                "sup_id": supplier_schema.dump(x[3]) if x[3] else None,
                "ord_id": fkpb_schema.dump(x[4]) if x[4] else None,
                "ord_date": APCardSchema(only=["ord_date"]).dump(x[0])["ord_date"]
                if x[0]
                else None,
                "ord_due": APCardSchema(only=["ord_due"]).dump(x[0])["ord_due"]
                if x[0]
                else None,
                "po_id": po_schema.dump(x[2]) if x[2] else None,
                "acq_id": acq_schema.dump(x[1]) if x[1] else None,
                "acq_date": APCardSchema(only=["acq_date"]).dump(x[0])["acq_date"]
                if x[0]
                else None,
                "cur_conv": x[0].cur_conv,
                "trx_dbcr": x[0].trx_dbcr,
                "trx_type": x[0].trx_type,
                "pay_type": x[0].pay_type,
                "trx_amnh": x[0].trx_amnh,
                "trx_amnv": x[0].trx_amnv,
                "acq_amnh": x[0].acq_amnh,
                "acq_amnv": x[0].acq_amnv,
                "giro_id": giro_schema.dump(x[5]) if x[5] else None,
                "giro_date": APCardSchema(only=["giro_date"]).dump(x[0])["giro_date"]
                if x[0]
                else None,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/arcard", methods=["GET"])
@token_required
def arcard(self):
    ar = (
        db.session.query(ArCard, AcqDdb, OrdpjHdb, CustomerMdb, LocationMdb, GiroHdb)
        .outerjoin(AcqDdb, AcqDdb.id == ArCard.acq_id)
        .outerjoin(OrdpjHdb, OrdpjHdb.id == ArCard.bkt_id)
        .outerjoin(CustomerMdb, CustomerMdb.id == ArCard.cus_id)
        .outerjoin(LocationMdb, LocationMdb.id == ArCard.loc_id)
        .outerjoin(GiroHdb, GiroHdb.id == ArCard.giro_id)
        .all()
    )

    final = []
    for x in ar:
        final.append(
            {
                "id": x[0].id,
                "cus_id": customer_schema.dump(x[3]) if x[3] else None,
                "trx_code": x[0].trx_code,
                "trx_date": ARCardSchema(only=["trx_date"]).dump(x[0])["trx_date"]
                if x[0]
                else None,
                "trx_due": ARCardSchema(only=["trx_date"]).dump(x[0])["trx_date"]
                if x[0]
                else None,
                "acq_id": acq_schema.dump(x[1]) if x[1] else None,
                "acq_date": AcqSchema(only=["acq_date"]).dump(x[1])["acq_date"]
                if x[1]
                else None,
                "bkt_id": ordpj_schema.dump(x[2]) if x[2] else None,
                "bkt_date": OrdpjSchema(only=["trx_date"]).dump(x[2])["trx_date"]
                if x[2]
                else None,
                "cur_conv": x[0].cur_conv,
                "trx_dbcr": x[0].trx_dbcr,
                "trx_type": x[0].trx_type,
                "pay_type": x[0].pay_type,
                "trx_amnh": x[0].trx_amnh,
                "trx_amnv": x[0].trx_amnv,
                "acq_amnh": acq_schema.dump(x[1]) if x[1] else None,
                "acq_amnv": acq_schema.dump(x[1]) if x[1] else None,
                "bkt_amnv": ordpj_schema.dump(x[2]) if x[2] else None,
                "bkt_amnh": ordpj_schema.dump(x[2]) if x[2] else None,
                "trx_desc": x[0].trx_desc,
                "pos_flag": x[0].pos_flag,
                "loc_id": loct_schema.dump(x[4]) if x[4] else None,
                "trx_pymnt": x[0].trx_pymnt,
                "giro_id": giro_schema.dump(x[5]) if x[5] else None,
                "giro_date": GiroSchema(only=["giro_date"]).dump(x[5])["giro_date"]
                if x[5]
                else None,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/dashboard-info", methods=["GET"])
@token_required
def dashboard_info(self):
    po = PoMdb.query.filter(PoMdb.status == 0).all()
    so = SordHdb.query.filter(SordHdb.status == 0).all()

    ap_card = ApCard.query.all()
    ar_card = ArCard.query.all()
    ap = (
        db.session.query(extract("month", ApCard.ord_date), func.sum(ApCard.trx_amnh))
        .filter(and_(ApCard.trx_type == "LP", ApCard.pay_type == "P1"))
        .group_by(extract("month", ApCard.ord_date))
        .all()
    )
    ar = (
        db.session.query(extract("month", ArCard.trx_date), func.sum(ArCard.trx_amnh))
        .filter(and_(ArCard.trx_type == "JL", ArCard.pay_type == "P1"))
        .group_by(extract("month", ArCard.trx_date))
        .all()
    )

    lns_ap = (
        db.session.query(extract("month", ApCard.ord_date), func.sum(ApCard.acq_amnh))
        .filter(and_(ApCard.trx_type == "LP", ApCard.pay_type == "H4"))
        .group_by(extract("month", ApCard.ord_date))
        .all()
    )
    lns_ar = (
        db.session.query(extract("month", ArCard.trx_date), func.sum(ArCard.acq_amnh))
        .filter(and_(ArCard.trx_type == "JL", ArCard.pay_type == "H4"))
        .group_by(extract("month", ArCard.trx_date))
        .all()
    )

    trans = (
        db.session.query(TransDdb, AccouMdb)
        .outerjoin(AccouMdb, AccouMdb.id == TransDdb.acc_id)
        .filter(AccouMdb.kat_code.in_((14, 15, 16, 17, 18, 19)))
        .all()
    )

    kewajiban = 0

    for x in trans:
        kewajiban += x[0].trx_amnt

    pur_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sls_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    ap_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ar_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for x in ap:
        pur_list[int(x[0]) - 1] = x[1]
        if lns_ap:
            for y in lns_ap:
                if x[0] == y[0]:
                    ap_list[int(x[0]) - 1] = x[1] - y[1]
        else:
            ap_list[int(x[0]) - 1] = x[1]

    for x in ar:
        sls_list[int(x[0] - 1)] = x[1]
        if lns_ar:
            for y in lns_ar:
                if x[0] == y[0]:
                    ar_list[int(x[0]) - 1] = x[1] - y[1]
        else:
            ar_list[int(x[0]) - 1] = x[1]

    total_ap = 0
    total_lns = 0

    for x in ap_card:
        if x.trx_type == "LP" and x.pay_type == "P1":
            total_ap += x.trx_amnh
        elif x.trx_type == "LP" and x.pay_type == "H4":
            total_lns += x.acq_amnh

    total_ar = 0
    ar_lns = 0
    for x in ar_card:
        if x.trx_type == "JL" and x.pay_type == "P1":
            total_ar += x.trx_amnh
        elif x.trx_type == "JL" and x.pay_type == "H4":
            ar_lns += x.acq_amnh

    result = {
        "out_pur": len(po) if po else 0,
        "ap": total_ap - total_lns,
        "out_sls": len(so) if so else 0,
        "ar": total_ar - ar_lns,
        "pur_list": pur_list,
        "sls_list": sls_list,
        "ap_list": ap_list,
        "ar_list": ar_list,
        "assets": 0,
        "kewajiban": kewajiban,
        "modal": 3713300,
    }

    return response(200, "Berhasil", True, result)


@app.route("/v1/api/trans", methods=["GET"])
@token_required
def trans(self):
    trn = (
        db.session.query(TransDdb, AccouMdb, CcostMdb, ProjMdb, CurrencyMdb)
        .outerjoin(AccouMdb, AccouMdb.id == TransDdb.acc_id)
        .outerjoin(CcostMdb, CcostMdb.id == TransDdb.ccost_id)
        .outerjoin(ProjMdb, ProjMdb.id == TransDdb.proj_id)
        .outerjoin(CurrencyMdb, CurrencyMdb.id == TransDdb.cur_id)
        .all()
    )

    final = []
    for x in trn:
        final.append(
            {
                "id": x[0].id,
                "trx_code": x[0].trx_code,
                "trx_date": TransDDB(only=["trx_date"]).dump(x[0])["trx_date"]
                if x[0]
                else None,
                "acc_id": accou_schema.dump(x[1]) if x[1] else None,
                "ccost_id": ccost_schema.dump(x[2]) if x[2] else None,
                "proj_id": proj_schema.dump(x[3]) if x[3] else None,
                "acq_date": TransDDB(only=["acq_date"]).dump(x[0])["acq_date"]
                if x[0]
                else None,
                "cur_rate": currency_schema.dump(x[4]) if x[4] else None,
                "trx_vala": x[0].trx_vala,
                "trx_amnt": x[0].trx_amnt,
                "trx_dbcr": x[0].trx_dbcr,
                "trx_desc": x[0].trx_desc,
                "gen_post": x[0].gen_post,
                "post_date": TransDDB(only=["post_date"]).dump(x[0])["post_date"],
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/giro", methods=["GET"])
@token_required
def giro(self):
    giro = (
        db.session.query(GiroHdb, BankMdb, SupplierMdb, ExpHdb)
        .outerjoin(BankMdb, BankMdb.id == GiroHdb.bank_id)
        .outerjoin(SupplierMdb, SupplierMdb.id == GiroHdb.sup_id)
        .outerjoin(ExpHdb, ExpHdb.id == GiroHdb.pay_code)
        .all()
    )

    final = []
    for x in giro:
        final.append(
            {
                "id": x[0].id,
                "giro_date": GiroSchema(only=["giro_date"]).dump(x[0])["giro_date"]
                if x[0]
                else None,
                "giro_num": x[0].giro_num,
                "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                "pay_code": exp_schema.dump(x[3]) if x[3] else None,
                "pay_date": GiroSchema(only=["pay_date"]).dump(x[0])["pay_date"]
                if x[0]
                else None,
                "sup_id": supplier_schema.dump(x[2]) if x[2] else None,
                "value": x[0].value,
                "status": x[0].status,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/giro/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def giro_id(self, id):
    giro = GiroHdb.query.filter(GiroHdb.id == id).first()
    if request.method == "PUT":
        try:
            giro_date = request.json["giro_date"]
            giro_num = request.json["giro_num"]
            bank_id = request.json["bank_id"]
            pay_code = request.json["pay_code"]
            pay_date = request.json["pay_date"]
            sup_id = request.json["sup_id"]
            value = request.json["value"]
            status = request.json["status"]

            giro.giro_date = giro_date
            giro.giro_num = giro_num
            giro.bank_id = bank_id
            giro.pay_code = pay_code
            giro.pay_date = pay_date
            giro.sup_id = sup_id
            giro.value = value
            giro.status = status

            db.session.commit()

            result = response(200, "Berhasil", True, giro_schema.dump(giro))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    elif request.method == "DELETE":
        db.session.delete(giro)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        result = (
            db.session.query(GiroHdb, BankMdb, SupplierMdb, ExpHdb)
            .outerjoin(BankMdb, BankMdb.id == GiroHdb.bank_id)
            .outerjoin(SupplierMdb, SupplierMdb.id == GiroHdb.sup_id)
            .outerjoin(ExpHdb, ExpHdb.id == GiroHdb.pay_code)
            .order_by(GiroHdb.id.asc())
            .filter(GiroHdb.id == id)
            .first()
        )
        data = {
            "giro": giro_schema.dump(result[0]),
            "bank": bank_schema.dump(result[1]),
            "supplier": supplier_schema.dump(result[2]),
            "exps": exp_schema.dump(result[3]),
        }

        return response(200, "Berhasil", True, data)


@app.route("/v1/api/approval", methods=["GET"])
@token_required
def approval(self):
    po = (
        db.session.query(PoMdb, PreqMdb, CcostMdb, SupplierMdb, RulesPayMdb)
        .outerjoin(PreqMdb, PreqMdb.id == PoMdb.preq_id)
        .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
        .outerjoin(SupplierMdb, SupplierMdb.id == PoMdb.sup_id)
        .outerjoin(RulesPayMdb, RulesPayMdb.id == PoMdb.top)
        .filter(PoMdb.apprv == False)
        .order_by(PoMdb.id.asc())
        .all()
    )

    pprod = (
        db.session.query(PprodDdb, ProdMdb, UnitMdb)
        .outerjoin(ProdMdb, ProdMdb.id == PprodDdb.prod_id)
        .outerjoin(UnitMdb, UnitMdb.id == PprodDdb.unit_id)
        .all()
    )

    pjasa = (
        db.session.query(PjasaDdb, JasaMdb, UnitMdb)
        .outerjoin(JasaMdb, JasaMdb.id == PjasaDdb.jasa_id)
        .outerjoin(UnitMdb, UnitMdb.id == PjasaDdb.unit_id)
        .all()
    )

    final = []
    for x in po:
        product = []
        for y in pprod:
            if y[0].po_id == x[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                product.append(pprod_schema.dump(y[0]))

        jasa = []
        for z in pjasa:
            if z[0].po_id == x[0].id:
                z[0].jasa_id = jasa_schema.dump(z[1])
                z[0].unit_id = unit_schema.dump(z[2])
                jasa.append(pjasa_schema.dump(z[0]))

        final.append(
            {
                "id": x[0].id,
                "po_code": x[0].po_code,
                "po_date": PoSchema(only=["po_date"]).dump(x[0])["po_date"],
                "preq_id": {
                    "id": x[1].id,
                    "req_code": x[1].req_code,
                    "req_date": PreqSchema(only=["req_date"]).dump(x[1])["req_date"],
                    "req_dep": ccost_schema.dump(x[2]) if x[2] else None,
                    "req_ket": x[1].req_ket,
                    "status": x[1].status,
                }
                if x[1]
                else None,
                "ppn_type": x[0].ppn_type,
                "sup_id": supplier_schema.dump(x[3]) if x[3] else None,
                "top": rpay_schema.dump(x[4]) if x[4] else None,
                "due_date": PoSchema(only=["due_date"]).dump(x[0])["due_date"]
                if x[0].due_date
                else None,
                "split_inv": x[0].split_inv,
                "prod_disc": x[0].prod_disc,
                "jasa_disc": x[0].jasa_disc,
                "total_disc": x[0].total_disc,
                "status": x[0].status,
                "apprv": x[0].apprv,
                "print": x[0].print,
                "pprod": product,
                "pjasa": jasa,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/approval/<int:id>", methods=["GET"])
@token_required
def update_approval(self, id):
    po = PoMdb.query.filter(PoMdb.id == id).first()

    po.apprv = True

    db.session.commit()

    return response(200, "Berhasil", True, None)


@app.route("/v1/api/balance", methods=["GET"])
@token_required
def balance(self):
    cash = AccouMdb.query.filter(AccouMdb.kat_code == 1).all()

    saldo_cash = 0
    for x in cash:
        saldo_cash += x.sld_awal

    return response(200, "Berhasil", True, {"cash": saldo_cash})


@app.route("/v1/api/stcard", methods=["GET"])
@token_required
def st_card(self):
    st = (
        db.session.query(StCard, ProdMdb, LocationMdb)
        .outerjoin(ProdMdb, ProdMdb.id == StCard.prod_id)
        .outerjoin(LocationMdb, LocationMdb.id == StCard.loc_id)
        .order_by(StCard.trx_date.asc())
        .all()
    )

    final = []
    for x in st:
        x[0].prod_id = prod_schema.dump(x[1]) if x[1] else None
        x[0].loc_id = loct_schema.dump(x[2]) if x[2] else None
        final.append(st_card_schema.dump(x[0]))

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/price-history", methods=["GET"])
@token_required
def price_history(self):
    history = (
        db.session.query(HrgBlMdb, OrdpbHdb, SupplierMdb, ProdMdb)
        .outerjoin(OrdpbHdb, OrdpbHdb.id == HrgBlMdb.ord_id)
        .outerjoin(SupplierMdb, SupplierMdb.id == HrgBlMdb.sup_id)
        .outerjoin(ProdMdb, ProdMdb.id == HrgBlMdb.prod_id)
        .all()
    )

    final = [
        {
            "id": x[0].id,
            "order": dord_schema.dump(x[1]),
            "supplier": supplier_schema.dump(x[2]),
            "product": prod_schema.dump(x[3]),
            "price": x[0].price,
        }
        for x in history
    ]

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/mesin", methods=["GET", "POST"])
@token_required
def mesin(self):
    if request.method == "POST":
        try:
            msn_code = request.json["msn_code"]
            msn_name = request.json["msn_name"]
            desc = request.json["desc"]

            mesin = MsnMdb(msn_code, msn_name, desc)

            db.session.add(mesin)
            db.session.commit()

            result = response(200, "Berhasil", True, msn_schema.dump(mesin))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        mesin = MsnMdb.query.order_by(MsnMdb.id.desc()).all()

        return response(200, "Berhasil", True, msns_schema.dump(mesin))


@app.route("/v1/api/mesin/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def mesin_id(self, id):
    mesin = MsnMdb.query.filter(MsnMdb.id == id).first()
    if request.method == "PUT":
        try:
            msn_code = request.json["msn_code"]
            msn_name = request.json["msn_name"]
            desc = request.json["desc"]

            mesin.msn_code = msn_code
            mesin.msn_name = msn_name
            mesin.desc = desc

            db.session.commit()

            result = response(200, "Berhasil", True, msn_schema.dump(mesin))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        if mesin:
            db.session.delete(mesin)
            db.session.commit()

            return response(200, "Berhasil", True, None)

        return response(400, "Data Tidak Ditemukan", False, None)
    else:
        return response(200, "Berhasil", True, msn_schema.dump(mesin))


@app.route("/v1/api/formula", methods=["GET", "POST"])
@token_required
def formula(self):
    if request.method == "POST":
        try:
            fcode = request.json["fcode"]
            fname = request.json["fname"]
            version = request.json["version"]
            rev = request.json["rev"]
            desc = request.json["desc"]
            active = request.json["active"]
            date_created = request.json["date_created"]
            product = request.json["product"]
            material = request.json["material"]

            form = FprdcHdb(fcode, fname, version, rev, desc, active, date_created)

            db.session.add(form)
            db.session.commit()

            new_product = []
            for x in product:
                if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                    new_product.append(
                        FprodDdb(
                            form.id, x["prod_id"], x["unit_id"], x["qty"], x["aloc"]
                        )
                    )

            new_material = []
            for x in material:
                if x["prod_id"] and x["unit_id"] and x["qty"] and int(x["qty"]) > 0:
                    new_material.append(
                        FmtrlDdb(
                            form.id, x["prod_id"], x["unit_id"], x["qty"], x["price"]
                        )
                    )

            if len(new_product) > 0:
                db.session.add_all(new_product)

            if len(new_material) > 0:
                db.session.add_all(new_material)

            db.session.commit()

            result = response(200, "Berhasil", True, fprdc_schema.dump(form))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        form = FprdcHdb.query.order_by(FprdcHdb.date_updated.desc()).all()

        product = (
            db.session.query(FprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
            .all()
        )

        material = (
            db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
            .all()
        )

        final = []
        for x in form:
            prod = []
            for y in product:
                if x.id == y[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    prod.append(fprod_schema.dump(y[0]))

            mtrl = []
            for y in material:
                if x.id == y[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    mtrl.append(fmtrl_schema.dump(y[0]))

            final.append(
                {
                    "id": x.id,
                    "fcode": x.fcode,
                    "fname": x.fname,
                    "version": x.version,
                    "rev": x.rev,
                    "desc": x.desc,
                    "active": x.active,
                    "date_created": FprdcSchema(only=["date_created"]).dump(x)[
                        "date_created"
                    ],
                    "date_updated": FprdcSchema(only=["date_updated"]).dump(x)[
                        "date_updated"
                    ],
                    "product": prod,
                    "material": mtrl,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/formula/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def formula_id(self, id):
    x = FprdcHdb.query.filter(FprdcHdb.id == id).first()
    if request.method == "PUT":
        try:
            fcode = request.json["fcode"]
            fname = request.json["fname"]
            version = request.json["version"]
            rev = request.json["rev"]
            desc = request.json["desc"]
            active = request.json["active"]
            product = request.json["product"]
            material = request.json["material"]

            x.fcode = fcode
            x.fname = fname
            x.version = version
            x.rev = rev
            x.desc = desc
            x.active = active

            db.session.commit()

            old_prod = FprodDdb.query.filter(FprodDdb.form_id == id).all()
            new_product = []
            for y in old_prod:
                for z in product:
                    if z["id"]:
                        if z["id"] == y.id:
                            if (
                                z["id"]
                                and z["prod_id"]
                                and z["unit_id"]
                                and z["qty"]
                                and int(z["qty"]) > 0
                            ):
                                y.prod_id = z["prod_id"]
                                y.unit_id = z["unit_id"]
                                y.qty = z["qty"]
                                y.aloc = z["aloc"]
                    else:
                        if (
                            z["prod_id"]
                            and z["unit_id"]
                            and z["qty"]
                            and int(z["qty"]) > 0
                        ):
                            new_product.append(
                                FprodDdb(
                                    z.id,
                                    z["prod_id"],
                                    z["unit_id"],
                                    z["qty"],
                                    z["aloc"],
                                )
                            )

            old_material = FmtrlDdb.query.filter(FmtrlDdb.form_id == id).all()
            new_material = []
            for y in old_material:
                for z in material:
                    if z["id"]:
                        if z["id"] == y.id:
                            if (
                                z["id"]
                                and z["prod_id"]
                                and z["unit_id"]
                                and z["qty"]
                                and int(z["qty"]) > 0
                            ):
                                y.prod_id = z["prod_id"]
                                y.unit_id = z["unit_id"]
                                y.qty = z["qty"]
                                y.price = z["price"]
                    else:
                        if (
                            z["prod_id"]
                            and z["unit_id"]
                            and z["qty"]
                            and int(z["qty"]) > 0
                        ):
                            new_material.append(
                                FmtrlDdb(
                                    z.id,
                                    z["prod_id"],
                                    z["unit_id"],
                                    z["qty"],
                                    z["price"],
                                )
                            )

            if len(new_product) > 0:
                db.session.add_all(new_product)

            if len(new_material) > 0:
                db.session.add_all(new_material)

            db.session.commit()

            result = response(200, "Berhasil", True, fprdc_schema.dump(x))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        old_prod = FprodDdb.query.filter(FprodDdb.form_id == id).all()
        old_material = FmtrlDdb.query.filter(FmtrlDdb.form_id == id).all()

        for y in old_prod:
            db.session.delete(y)

        for y in old_material:
            db.session.delete(y)

        db.session.delete(x)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        product = (
            db.session.query(FprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
            .filter(FprodDdb.form_id == id)
            .all()
        )

        material = (
            db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
            .filter(FprodDdb.form_id == id)
            .all()
        )

        final = []
        prod = []
        for y in product:
            if x.id == y[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                prod.append(fprod_schema.dump(y[0]))

        mtrl = []
        for y in material:
            if x.id == y[0].id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                mtrl.append(fmtrl_schema.dump(y[0]))

        final = {
            "id": x.id,
            "fcode": x.fcode,
            "fname": x.fname,
            "version": x.version,
            "rev": x.rev,
            "desc": x.desc,
            "active": x.active,
            "date_created": FprdcSchema(only=["date_created"]).dump(x)["date_created"],
            "date_updated": FprdcSchema(only=["date_updated"]).dump(x)["date_updated"],
            "product": prod,
            "material": mtrl,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/planning", methods=["GET", "POST"])
@token_required
def planning(self):
    if request.method == "POST":
        try:
            pcode = request.json["pcode"]
            pname = request.json["pname"]
            form_id = request.json["form_id"]
            desc = request.json["desc"]
            date_planing = request.json["date_planing"]
            total = request.json["total"]
            unit = request.json["unit"]
            mesin = request.json["mesin"]

            plan = PlanHdb(pcode, pname, form_id, desc, date_planing, total, unit)

            db.session.add(plan)
            db.session.commit()

            new_mesin = []
            for x in mesin:
                if x["mch_id"]:
                    new_mesin.append(PlmchDdb(plan.id, x["mch_id"]))

            if len(new_mesin) > 0:
                db.session.add_all(new_mesin)

            db.session.commit()

            result = response(200, "Berhasil", True, plan_schema.dump(plan))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        plan = (
            db.session.query(PlanHdb, FprdcHdb, UnitMdb)
            .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
            .outerjoin(UnitMdb, UnitMdb.id == PlanHdb.unit)
            .order_by(PlanHdb.id.desc())
            .all()
        )

        product = (
            db.session.query(FprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
            .all()
        )

        material = (
            db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
            .all()
        )

        mesin = (
            db.session.query(PlmchDdb, MsnMdb)
            .outerjoin(MsnMdb, MsnMdb.id, PlmchDdb)
            .all()
        )

        final = []
        for x in plan:
            prod = []
            for y in product:
                if x[1].id == y[0].form_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    prod.append(fprod_schema.dump(y[0]))

            mat = []
            for y in material:
                if x[1].id == y[0].form_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    mat.append(fmtrl_schema.dump(y[0]))

            msn = []
            for y in mesin:
                if x[0].id == y[0].pl_id:
                    y[0].mch_id = msn_schema.dump(y[1])
                    msn.append(plmch_schema.dump(y[0]))

            final.append(
                {
                    "id": x[0].id,
                    "pcode": x[0].pcode,
                    "pname": x[0].pname,
                    "form_id": fprdc_schema.dump(x[1]),
                    "desc": x[0].desc,
                    "date_created": PlanSchema(only=["date_creaded"]).dump(x[0])[
                        "date_created"
                    ],
                    "date_planing": PlanSchema(only=["date_planing"]).dump(x[0])[
                        "date_planing"
                    ],
                    "total": x[0].total,
                    "unit": units_schema.dump(x[2]),
                    "material": mat,
                    "product": prod,
                    "mesin": msn,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/planning/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def planning_id(self, id):
    x = PlanHdb.query.filter(PlanHdb.id == id).first()
    if request.method == "PUT":
        try:
            pcode = request.json["pcode"]
            pname = request.json["pname"]
            form_id = request.json["form_id"]
            desc = request.json["desc"]
            date_planing = request.json["date_planing"]
            total = request.json["total"]
            unit = request.json["unit"]
            mesin = request.json["mesin"]

            x.pcode = pcode
            x.pname = pname
            x.form_id = form_id
            x.desc = desc
            x.date_planing = date_planing
            x.total = total
            x.unit = unit

            db.session.commit()

            old_mesin = PlmchDdb.query.filter(PlmchDdb.pl_id == id).all()
            new_mesin = []

            for z in mesin:
                if z["id"]:
                    for y in old_mesin:
                        if z["id"] == y.id:
                            if z["mch_id"]:
                                y.mch_id = z["mch_id"]
                else:
                    if z["mch_id"]:
                        new_mesin.append(PlmchDdb(id, x["mch_id"]))

            if len(new_mesin) > 0:
                db.session.add_all(new_mesin)

            db.session.commit()

            result = response(200, "Berhasil", True, plan_schema.dump(x))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        old_mesin = PlmchDdb.query.filter(PlmchDdb.pl_id == id).all()

        for y in old_mesin:
            db.session.delete(y)

        db.session.delete(x)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        x = (
            db.session.query(PlanHdb, FprdcHdb, UnitMdb)
            .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
            .outerjoin(UnitMdb, UnitMdb.id == PlanHdb.unit)
            .filter(PlanHdb.id == id)
            .first()
        )

        product = (
            db.session.query(FprodDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
            .all()
        )

        material = (
            db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
            .all()
        )

        mesin = (
            db.session.query(PlmchDdb, MsnMdb)
            .outerjoin(MsnMdb, MsnMdb.id, PlmchDdb)
            .all()
        )

        prod = []
        for y in product:
            if x[1].id == y[0].form_id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                prod.append(fprod_schema.dump(y[0]))

        mat = []
        for y in material:
            if x[1].id == y[0].form_id:
                y[0].prod_id = prod_schema.dump(y[1])
                y[0].unit_id = unit_schema.dump(y[2])
                mat.append(fmtrl_schema.dump(y[0]))

        msn = []
        for y in mesin:
            if x[0].id == y[0].pl_id:
                y[0].mch_id = msn_schema.dump(y[1])
                msn.append(plmch_schema.dump(y[0]))

        final = {
            "id": x[0].id,
            "pcode": x[0].pcode,
            "pname": x[0].pname,
            "form_id": fprdc_schema.dump(x[1]),
            "desc": x[0].desc,
            "date_created": PlanSchema(only=["date_creaded"]).dump(x[0])[
                "date_created"
            ],
            "date_planing": PlanSchema(only=["date_planing"]).dump(x[0])[
                "date_planing"
            ],
            "total": x[0].total,
            "unit": units_schema.dump(x[2]),
            "material": mat,
            "product": prod,
            "mesin": msn,
        }

        return response(200, "Berhasil", True, final)
