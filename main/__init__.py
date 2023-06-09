from lib2to3.pgen2 import token
import time
from datetime import datetime
from unicodedata import name
from flask import Flask, redirect, request, jsonify, send_from_directory
import requests

from .function.produksi.batch.batch import Batch
from .function.produksi.batch.batch_id import BatchId
from .function.produksi.formula.formula import Formula
from .function.produksi.formula.formula_id import FormulaId
from .function.produksi.pembebanan.pembebanan import Pembebanan
from .function.produksi.pembebanan.pembebanan_id import PembebananId
from .function.produksi.penerimaan_hasil_jadi.phj import PenerimaanHasilJadi
from .function.produksi.penerimaan_hasil_jadi.phj_id import PenerimaanHasilJadiId
from .function.produksi.planning.planning import Planning
from .function.produksi.planning.planning_id import PlanningId
from .function.account.account import Account
from .function.account.account_id import AccountId
from .function.update_table import UpdateTable
from .model.prod_supp_ddb import ProdSupDdb
from .schema.prod_sup_ddb import *
from .function.kategory.kategory_import import KategoryImport
from .function.cost_center.cost_center import CostCenter
from .function.account.account_filter import AccountFilter
from .function.cost_center.cost_center_filter import CcostFilter
from .function.delete_ap_payment import DeleteApPayment
from .function.income.income import Income
from .function.income.income_id import IncomeId
from .function.koreksi_sto.koreksi_sto import KoreksiPersediaan
from .function.koreksi_sto.koreksi_sto_id import KorPersediaanId
from .function.menu.menu import Menu
from .function.menu.menu_id import MenuId
from .function.kategory.kategory import Kategory
from .function.kategory.kategory_id import KategoryId
from .function.retur_order.retur_id import ReturOrderId
from .function.retur_order.retur_order import ReturOrder
from .function.retur_sales.retur_id import ReturSaleId
from .function.retur_sales.retur_sales import ReturSale
from .function.update_ap_giro import UpdateApGiro
from .function.update_ap_payment import UpdateApPayment
from .function.update_ar import UpdateAr
from .function.update_ar_giro import UpdateArGiro
from .function.update_batch import updateBatch
from .function.purchase_order.po import PurchaseOrder
from .function.purchase_order.po_id import PurchaseOrderId
from .function.purchase_order.close_po import PurchaseOrderClose
from .function.order.order import Order
from .function.order.order_id import OrderId
from .function.order.invoice_pb import InvoicePb
from .function.order.invoice_pb_id import InvoicePbId
from .function.order.faktur_pb import FakturPb
from .function.order.faktur_pb_id import FakturPbId
from .function.sales_order.so import SalesOrder
from .function.sales_order.so_id import SalesOrderId
from .function.sales_order.close_so import SalesOrderClose
from .function.sale.sale import Sale
from .function.sale.sale_id import SaleId
from .function.sale.invoice_sl import InvoicePj
from .function.sale.invoice_sl_id import InvoicePjId
from .function.sale.faktur_sl import FakturPj
from .function.sale.faktur_sl_id import FakturPjId
from .function.expense.expense import Expense
from .function.expense.expense_id import ExpenseId
from .function.saldo_awal.saldo_awal import SaldoInv
from .function.saldo_awal.saldo_awal_ap import SaldoAP
from .function.saldo_awal.saldo_awal_ap_id import SaldoAPId
from .function.saldo_awal.saldo_awal_ar import SaldoAR
from .function.saldo_awal.saldo_awal_ar_id import SaldoARId
from .function.saldo_awal.saldo_awal_gl import SaldoAwalGl
from .function.saldo_awal.saldo_awal_gl_sts import SaldoAwalGlStatus
from .function.setup.setup_sa import SetupSldAkhir
from .function.setup.setup_sa_id import SetupSaId
from .function.saldo_akhir.saldo_akhir import SaldoAkhir, SaldoAkhirId
from .function.posting.posting_ym import GetYearPosting
from .function.posting.posting import Posting
from .function.posting.unpost import Unpost
from .function.posting.trasfer import TransferGL
from .function.posting.closing import Closing
from .function.koreksi_hutang.koreksi_hutang import KoreksiHutang
from .function.koreksi_hutang.koreksi_hutang_id import KoreksiHutangId
from .function.koreksi_piutang.koreksi_piutang import KoreksiPiutang
from .function.koreksi_piutang.koreksi_piutang_id import KoreksiPiutangId
from .function.group_product.group_product import GroupProduct
from .function.group_product.group_product_id import GroupProductId
from .function.request_purchase.rp import RequestPurchase
from .function.request_purchase.rp_id import RequestPurchaseId
from .model.giro_inc_hdb import GiroIncHdb
from .model.iacq_ddb import IAcqDdb
from .model.inc_hdb import IncHdb
from .model.main_menu import MainMenu
from .model.neraca_ddb import NeracaDdb
from .model.neraca_exept_ddb import NeracaEceptionDdb
from .model.neraca_hdb import NeracaHdb
from .model.ovh_ddb import OvhDdb
from .model.user_menu import UserMenu
from .model.user_model import UserModel
from .schema.inc_hdb import inc_schema
from .function.update_mutasi import UpdateMutasi
from .function.update_pembelian import UpdatePembelian
from .function.update_rpbb import UpdateRpbb
from .function.update_stock import UpdateStock
from .model.accou_mdb import AccouMdb
from .model.acq_ddb import AcqDdb
from .model.adm_user_menu import AdmUserMenu
from .model.adm_menu import AdmMenu
from .model.apcard_mdb import ApCard
from .model.arcard_mdb import ArCard
from .model.bank_mdb import BankMdb
from .model.batch_mdb import BatchMdb
from .model.ccost_mdb import CcostMdb
from .model.comp_mdb import CompMdb
from .model.djasa_ddb import DjasaDdb
from .model.exp_ddb import ExpDdb
from .model.exp_hdb import ExpHdb
from .model.fkpb_hdb import FkpbHdb
from .model.fmtrl_ddb import FmtrlDdb
from .model.fprdc_hdb import FprdcHdb
from .model.fprod_ddb import FprodDdb
from .model.giro_hdb import GiroHdb
from .model.hrgbl_mdb import HrgBlMdb
from .model.jjasa_ddb import JjasaDdb
from .model.jprod_ddb import JprodDdb
from .model.msn_mdb import MsnMdb
from .model.mtsi_ddb import MtsiDdb
from .model.mtsi_hdb import MtsiHdb
from .model.ordpb_hdb import OrdpbHdb
from .model.dprod_ddb import DprodDdb
from .model.group_prod_mdb import GroupProMdb
from .model.jasa_mdb import JasaMdb
from .model.jpel_mdb import JpelMdb
from .model.jpem_mdb import JpemMdb
from .model.ordpj_hdb import OrdpjHdb
from .model.phj_hdb import PhjHdb
from .model.pbb_hdb import PbbHdb
from .model.pjasa_ddb import PjasaDdb
from .model.plan_hdb import PlanHdb
from .model.plmch_ddb import PlmchDdb
from .model.po_mdb import PoMdb
from .model.po_sup_ddb import PoSupDdb
from .model.uph_ddb import UphDdb
from .model.pphj_ddb import PphjDdb
from .model.pprod_ddb import PprodDdb
from .model.preq_mdb import PreqMdb
from .model.prod_mdb import ProdMdb
from .model.reprod_ddb import ReprodDdb
from .model.retord_hdb import RetordHdb
from .model.rjasa_mdb import RjasaMdb

# from .model.rpbb_ddb import RpbbDdb
from .model.rpbb_ddb import RpbbDdb
from .model.rpbb_mdb import RpbbMdb
from .model.rphj_ddb import RphjDdb
from .model.rprod_mdb import RprodMdb
from .model.sales_mdb import SalesMdb
from .model.area_penjualan_mdb import AreaPenjualanMdb
from .model.setup_mdb import SetupMdb
from .model.sjasa_ddb import SjasaDdb
from .model.sord_hdb import SordHdb
from .model.sprod_ddb import SprodDdb
from .model.stcard_mdb import StCard
from .model.sub_area_mdb import SubAreaMdb
from .model.klasi_mdb import KlasiMdb
from .model.kateg_mdb import KategMdb
from .model.proj_mdb import ProjMdb
from .model.currency_mdb import CurrencyMdb
from .model.syarat_bayar_mdb import RulesPayMdb
from .model.lokasi_mdb import LocationMdb
from .model.custom_mdb import CustomerMdb
from .model.supplier_mdb import SupplierMdb
from .model.unit_mdb import UnitMdb
from .model.divisi_mdb import DivisionMdb
from .model.group_prod_mdb import GroupProMdb
from .model.pajak_mdb import PajakMdb
from .model.retsale_hdb import RetSaleHdb
from .model.apcard_mdb import ApCard
from .model.transddb import TransDdb
from .model.po_sup_ddb import PoSupDdb
from .model.memo_ddb import MemoDdb
from .model.memo_hdb import MemoHdb
from .model.neraca_mdb import NeracaMdb
from .model.pnl_mdb import PnlMdb
from .schema.pnl_mdb import pnl_schema, pnls_schema, PnlSchema
from .schema.neraca_mdb import neraca_schema, neracas_schema, NeracaSchema
from .schema.apcard_mdb import apcard_schema, apcards_schema, APCardSchema
from .schema.arcard_mdb import ARCardSchema
from .schema.ccost_mdb import ccost_schema, ccosts_schema, CcostSchema
from .schema.proj_mdb import proj_schema, projs_schema, ProjSchema
from .schema.rpbb_mdb import rpbb_schema
from .shared.shared import db
from .model.user import User
from .schema.user import user_schema, users_schema
from .schema.bank_mdb import bank_schema
from .schema.unit_mdb import unit_schema, units_schema, UnitSchema
from .schema.prod_mdb import prod_schema
from .schema.po_sup_ddb import poSup_schema
from .schema.fprdc_hdb import fprdc_schema, FprdcSchema
from .schema.fprod_ddb import fprod_schema
from .schema.fmtrl_ddb import fmtrl_schema
from .schema.memo_ddb import mddb_schema
from .schema.memo_hdb import mhdb_schema, MhdbSchema
from .schema.adm_user_menu import (
    AdmUserMenuSchema,
)
from .schema.klasi_mdb import klasi_schema, klasies_schema, KlasiMdb as KlasiSchema
from .schema.kateg_mdb import kateg_schema, kategs_schema, KategMdb as KategSchema
from .schema.accou_mdb import accou_schema, accous_schema, AccouSchema
from .schema.jpel_mdb import jpels_schema, jpel_schema
from .schema.jpem_mdb import jpems_schema, jpem_schema
from .schema.sales_mdb import saless_schema, sales_schema
from .schema.area_penjualan_mdb import area_penjualans_schema, area_penjualan_schema
from .schema.sub_area_mdb import sub_areas_schema, sub_area_schema
from .schema.currency_mdb import currencys_schema, currency_schema
from .schema.syarat_bayar_mdb import rpays_schema, rpay_schema
from .schema.lokasi_mdb import locts_schema, loct_schema
from .schema.comp_mdb import comp_shcema, comps_schema, CompSchema
from .schema.custom_mdb import customer_schema, customers_schema
from .schema.supplier_mdb import supplier_schema, suppliers_schema
from .schema.divisi_mdb import division_schema, divisions_schema
from .schema.group_prod_mdb import groupPro_schema, groupPros_schema
from .schema.pajak_mdb import pajk_schema, pajks_schema
from .schema.jasa_mdb import jasa_schema, jasas_schema
from .schema.preq_mdb import preq_schema, preqs_schema, PreqSchema
from .schema.rprod_mdb import rprod_schema, rprods_schema, RprodSchema
from .schema.rjasa_mdb import rjasa_schema, rjasas_schema, RjasaSchema
from .schema.pprod_ddb import pprod_schema, pprods_schema, PprodSchema
from .schema.pjasa_ddb import pjasa_schema, pjasas_schema, PjasaSchema
from .schema.sprod_ddb import sprod_schema, sprods_schema, SprodSchema
from .schema.sjasa_ddb import sjasa_schema, sjasas_schema, SjasaSchema
from .schema.po_mdb import po_schema, pos_schema, PoSchema
from .schema.sord_hdb import sord_schema, sords_schema, SordSchema
from .schema.dord_hdb import dord_schema, dords_schema, DordSchema
from .schema.dprod_ddb import dprod_schema, dprods_schema, DprodSchema
from .schema.djasa_ddb import djasa_schema, djasas_schema, DjasaSchema
from .schema.fkpb_hdb import fkpbs_schema, fkpb_schema, FkpbSchema
from .schema.retord_hdb import retord_schema, retords_schema, RetordSchema
from .schema.reprod_ddb import reprod_schema, reprods_schema, ReprodSchema
from .schema.ordpj_hdb import ordpj_schema, ordpjs_schema, OrdpjSchema
from .schema.jprod_ddb import jprod_schema, jprods_schema, JprodSchema
from .schema.jjasa_ddb import jjasa_schema, jjasas_schema, JjasaSchema
from .schema.exp_hdb import exp_schema, exps_schema, ExpSchema
from .schema.dexp_ddb import dexp_schema, dexps_schema, DexpSchema
from .schema.dacq_ddb import dacq_schema, dacqs_schema, DacqSchema
from .schema.iacq_ddb import iacq_schema, iacqs_schema, IacqSchema
from .schema.acq_ddb import acq_schema, acqs_schema, AcqSchema
from .schema.giro_hdb import giro_schema, giros_schema, GiroSchema
from .schema.giro_inc_hdb import grinc_schema, grincs_schema, GiroIncSchema
from .schema.apcard_mdb import apcard_schema, apcards_schema, APCardSchema
from .schema.retsale_hdb import retsale_schema, retsales_schema, RetSaleSchema
from .schema.transddb import trans_schema, transs_schema, TransDDB
from .schema.stcard_mdb import st_card_schema, st_cards_schema, StCardSchema
from .schema.msn_mdb import msns_schema, msn_schema, MsnSchema
from .schema.plan_hdb import plan_schema, plans_schema, PlanSchema
from .schema.plmch_ddb import plmch_schema, plmchs_schema, PlmchSchema
from .schema.batch_mdb import batch_schema, batchs_schema, BatchSchema
from .schema.phj_hdb import phj_schema, phjs_schema, PhjSchema
from .schema.pbb_hdb import pbb_schema, pbbs_schema, PbbSchema
from .schema.pphj_ddb import pphj_schema, pphjs_schema, PphjSchema
from .schema.uph_ddb import uph_schema, uphs_schema, UphSchema
from .schema.ovh_ddb import ovh_schema, ovhs_schema, OvhSchema
from .schema.rphj_ddb import rphj_schema, rphjs_schema, RphjSchema
from .schema.mtsi_hdb import mtsi_schema, mtsis_schema, MtsiSchema
from .schema.mtsi_ddb import mtsiddb_schema, mtsiddbs_schema, MtsiddbSchema
from .schema.setup_mdb import *
from sqlalchemy.exc import *
from sqlalchemy import and_, extract, func, or_, cast
from .shared.shared import server_name

import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from werkzeug.utils import secure_filename
import bcrypt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = Flask(__name__)


def target_url():
    return "https://itungin.id/"


def apiKey():
    return "42e8d306fd11942e83d509b631d52a48"


def cityUrl():
    return "https://api.rajaongkir.com/starter/city"


def authHelper():
    return os.getenv("AUTH_HELPER_URL")


def response(code, message, status, data):
    return (
        jsonify({"code": code, "status": status,
                "message": message, "data": data}),
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
            # user = User.query.filter(User.id == data["id"]).first()

            header = {"Authorization": "Bearer {}".format(token)}
            result = requests.get(
                url=authHelper() + "/user/" + str(data["id"]), headers=header
            ).json()

            if result["code"] == 200:
                user = UserModel(result["data"])
            elif result["code"] == 401:
                return response(401, "Invalid or expired token !!", False, None)
        except Exception as e:
            print(e)
            return response(401, "Invalid or expired token !!", False, None)
        # returns the current logged in users contex to the routes
        return f(user, *args, **kwargs)

    return decorated


@app.route("/")
def index():
    return redirect(target_url())


@app.route("/v1/api/login", methods=["POST"])
def login():
    result = requests.post(url="%s/login" %
                           (authHelper()), json=request.json).json()

    return response(result["code"], result["message"], result["status"], result["data"])
    # username = request.json["username"]
    # password = request.json["password"]
    # if "remember" in request.json:
    #     remember = request.json["remember"]
    # else:
    #     remember = False

    # user = User.query.filter(User.username == username).first()

    # if user is None:
    #     return response(403, "Akun tidak ditemukan", False, None)
    # else:
    #     if bcrypt.checkpw(password.encode(), user.password.encode()):
    #         if remember:
    #             token = jwt.encode(
    #                 {"id": user.id, "exp": datetime.utcnow() + timedelta(weeks=2)},
    #                 app.config["SECRET_KEY"],
    #             )
    #         else:
    #             token = jwt.encode(
    #                 {"id": user.id, "exp": datetime.utcnow() + timedelta(hours=5)},
    #                 app.config["SECRET_KEY"],
    #             )
    #         data = {"user": user_schema.dump(user), "token": token.decode("utf-8")}
    #         return response(200, "Berhasil", True, data)
    #     else:
    #         return response(403, "Password yang anda masukkan salah", False, None)


@app.route("/v1/api/user", methods=["POST", "GET"])
@token_required
def user(self):
    header = request.headers
    if request.method == "POST":
        request.json["company"] = self.company
        request.json["product"] = self.product
        request.json["endpoint_id"] = self.endpoint_id

        result = requests.post(
            url="%s/user" % (authHelper()),
            headers=header,
            json=request.json,
        ).json()

        if result["code"] == 200:
            user = UserModel(result["data"])
            try:
                menu = request.json["menu"]

                new_menu = []
                for x in menu:
                    if x["menu_id"]:
                        new_menu.append(
                            UserMenu(
                                user.id,
                                x["menu_id"],
                                x["view"],
                                x["edit"],
                                x["delete"],
                            )
                        )

                if len(new_menu) > 0:
                    db.session.add_all(new_menu)

                db.session.commit()

                return response(200, "Berhasil menambahkan user", True, result["data"])
            except IntegrityError:
                db.session.rollback()
                return response(400, "Gagal", False, None)
            except Exception as e:
                print(e)
                return response(400, str(e), False, str(e))
        else:
            return response(
                result["code"], result["message"], result["status"], result["data"]
            )
    else:
        result = requests.get(
            url="%s/user" % (authHelper()),
            headers=header,
        ).json()

        menus = UserMenu.query.order_by(UserMenu.id).all()
        users = []

        if result["code"] == 200:
            for x in result["data"]:
                menu = []
                for y in menus:
                    if x["id"] == y.user_id:
                        menu.append(
                            {
                                "menu_id": y.menu_id,
                                "view": y.view,
                                "edit": y.edit,
                                "delete": y.delete,
                            }
                        )
                users.append(
                    {
                        "id": x["id"],
                        "email": x["email"],
                        "username": x["username"],
                        "active": x["active"],
                        "menu": menu,
                    }
                )

            return response(200, "Berhasil", True, users)
        else:
            return response(
                result["code"], result["message"], result["status"], result["data"]
            )


@app.route("/v1/api/user/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def user_id(self, id):
    user = User.query.filter(User.id == id).first()
    if request.method == "PUT":
        old_menu = UserMenu.query.filter(UserMenu.user_id == id).all()
        if len(old_menu) > 0:
            for x in old_menu:
                db.session.delete(x)
            db.session.commit()

        menu = request.json["menu"]

        new_menu = []
        for x in menu:
            if x["menu_id"]:
                new_menu.append(
                    UserMenu(
                        id,
                        x["menu_id"],
                        x["view"],
                        x["edit"],
                        x["delete"],
                    )
                )

        if len(new_menu) > 0:
            db.session.add_all(new_menu)

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


@app.route("/v1/api/akses-menu", methods=["GET"])
@token_required
def access(self):
    user = (
        db.session.query(UserMenu, MainMenu)
        .outerjoin(MainMenu, MainMenu.id == UserMenu.menu_id)
        .filter(and_(UserMenu.user_id == self.id, MainMenu.visible == True))
        .order_by(MainMenu.category.asc(), MainMenu.id.asc())
        .all()
    )

    menu = []
    for x in user:
        sub_menu = []
        for y in user:
            last_menu = []
            for z in user:
                if z[1].parent_id == y[1].id:
                    last_menu.append(
                        {
                            "id": z[1].id,
                            "name": z[1].name,
                            "route_name": z[1].route_name,
                            "icon_file": z[1].icon_file,
                            "parent_id": z[1].parent_id,
                            "visible": z[1].visible,
                            "category": z[1].category,
                            "view": z[0].view,
                            "edit": z[0].edit,
                            "delete": z[0].delete,
                        }
                    )
            if y[1].parent_id == x[1].id:
                sub_menu.append(
                    {
                        "id": y[1].id,
                        "name": y[1].name,
                        "route_name": y[1].route_name,
                        "icon_file": y[1].icon_file,
                        "visible": y[1].visible,
                        "parent_id": y[1].parent_id,
                        "category": y[1].category,
                        "view": y[0].view,
                        "edit": y[0].edit,
                        "delete": y[0].delete,
                        "lastmenu": last_menu,
                    }
                )
        if not x[1].parent_id:
            menu.append(
                {
                    "id": x[1].id,
                    "name": x[1].name,
                    "route_name": x[1].route_name,
                    "icon_file": x[1].icon_file,
                    "visible": x[1].visible,
                    "parent_id": x[1].parent_id,
                    "category": x[1].category,
                    "view": x[0].view,
                    "edit": x[0].edit,
                    "delete": x[0].delete,
                    "submenu": sub_menu,
                }
            )

    menu = {
        "id": self.id,
        "email": self.email,
        "username": self.username,
        "name": self.name,
        "menu": menu,
    }

    return response(200, "Berhasil", True, menu)


@app.route("/v1/api/menu", methods=["POST", "GET"])
@token_required
def menu(self):
    return Menu(request)


@app.route("/v1/api/menu/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def menu_id(self, id):
    return MenuId(request, id)


@app.route("/v1/api/bank", methods=["POST", "GET"])
@token_required
def bank(self):
    return Bank(self, request)
    # if request.method == "POST":
    #     try:
    #         BANK_CODE = request.json["BANK_CODE"]
    #         ACC_ID = request.json["ACC_ID"]
    #         BANK_NAME = request.json["BANK_NAME"]
    #         BANK_DESC = request.json["BANK_DESC"]
    #         CURRENCY = request.json["CURRENCY"]
    #         bank = BankMdb(
    #             BANK_CODE, BANK_NAME, BANK_DESC, CURRENCY, ACC_ID, self.id, None
    #         )
    #         db.session.add(bank)
    #         db.session.commit()

    #         result = response(200, "Berhasil", True, bank_schema.dump(bank))
    #     except IntegrityError:
    #         db.session.rollback()
    #         result = response(400, "Kode sudah digunakan", False, None)
    #     finally:
    #         return result
    # else:
    #     result = (
    #         db.session.query(BankMdb, AccouMdb)
    #         .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
    #         .order_by(BankMdb.id.asc())
    #         .all()
    #     )
    #     data = [
    #         {"bank": bank_schema.dump(
    #             x[0]), "account": accou_schema.dump(x[1])}
    #         for x in result
    #     ]

    #     return response(200, "Berhasil", True, data)


@app.route("/v1/api/bank/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def bank_id(self, id):
    return BankId(id, request)
    # bank = BankMdb.query.filter(BankMdb.id == id).first()
    # if request.method == "PUT":
    #     bank.BANK_CODE = request.json["BANK_CODE"]
    #     bank.acc_id = request.json["ACC_ID"]
    #     bank.BANK_NAME = request.json["BANK_NAME"]
    #     bank.BANK_DESC = request.json["BANK_DESC"]
    #     bank.CURRENCY = request.json["CURRENCY"]
    #     db.session.commit()

    #     return response(200, "Berhasil", True, bank_schema.dump(bank))
    # elif request.method == "DELETE":
    #     db.session.delete(bank)
    #     db.session.commit()

    #     return response(200, "Berhasil", True, None)
    # else:
    #     result = (
    #         db.session.query(BankMdb, AccouMdb)
    #         .outerjoin(AccouMdb, BankMdb.BANK_ACC == AccouMdb.acc_code)
    #         .order_by(BankMdb.id.asc())
    #         .filter(BankMdb.id == id)
    #         .first()
    #     )
    #     data = {
    #         "bank": bank_schema.dump(result[0]),
    #         "account": accou_schema.dump(result[1]),
    #     }

    #     return response(200, "Berhasil", True, data)


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
    return Kategory(self, request)


@app.route("/v1/api/kategory/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def kategory_id(self, id):
    return KategoryId(id, request)


@app.route("/v1/api/import/kategori", methods=["POST"])
@token_required
def kateg_import(self):
    return KategoryImport(self, request)


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
            and_(
                AccouMdb.acc_code.like("%{}%".format(key)),
                AccouMdb.dou_type == "U",
                AccouMdb.umm_code == None,
            )
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


@app.route("/v1/api/account/su/<string:umm_code>", methods=["GET"])
@token_required
def account_sub_umum(self, umm_code):

    last_acc = (
        AccouMdb.query.filter(
            and_(AccouMdb.umm_code == umm_code, AccouMdb.dou_type == "U")
        )
        .order_by(AccouMdb.acc_code.desc())
        .first()
    )

    if last_acc != None:
        next_code = (
            umm_code + "0" +
            str(int(last_acc.acc_code.replace(umm_code, "")) + 1)
        )
    else:
        next_code = umm_code + "0" + "1"

    return response(200, "Berhasil", True, next_code)


@app.route("/v1/api/account/d/<string:umm_code>", methods=["GET"])
@token_required
def account_detail(self, umm_code):

    last_acc = (
        AccouMdb.query.filter(AccouMdb.umm_code == umm_code)
        .order_by(AccouMdb.id.desc(), AccouMdb.acc_code.desc())
        .first()
    )

    if last_acc != None:
        next_code = (
            umm_code + "." +
            str(int(last_acc.acc_code.replace(umm_code + ".", "")) + 1)
        )
        print(last_acc.acc_code)
        print(int(last_acc.acc_code.replace(umm_code + ".", "")))
    else:
        next_code = umm_code + "." + "1"
    return response(200, "Berhasil", True, next_code)


@app.route("/v1/api/account", methods=["POST", "GET"])
@token_required
def account(self):
    return Account(self, request)
    # if request.method == "POST":
    #     if "kode_acc" in request.json:
    #         acc_code = request.json["kode_acc"]
    #         acc_name = request.json["acc_name"]
    #         umm_code = request.json["kode_umum"]
    #         kat_code = request.json["kode_kategori"]
    #         dou_type = request.json["du"]
    #         sld_type = request.json["kode_saldo"]
    #         connect = request.json["terhubung"]
    #         sld_awal = request.json["saldo_awal"]
    #         level = request.json["level"]
    #         try:
    #             account = AccouMdb(
    #                 acc_code,
    #                 acc_name,
    #                 umm_code,
    #                 kat_code,
    #                 dou_type,
    #                 sld_type,
    #                 connect,
    #                 sld_awal,
    #                 level,
    #             )
    #             db.session.add(account)
    #             db.session.commit()
    #             result = response(200, "Berhasil", True,
    #                               accou_schema.dump(account))
    #         except IntegrityError:
    #             db.session.rollback()
    #             result = response(
    #                 400, "Kode akun " + acc_code + " sudah digunakan", False, None
    #             )
    #         finally:
    #             return result
    #     else:
    #         return response(406, "Data isian belum lengkap", False, None)
    # else:
    #     result = (
    #         db.session.query(AccouMdb, KategMdb, KlasiMdb)
    #         .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)
    #         .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
    #         # .order_by(KlasiMdb.id.asc())
    #         .order_by(KategMdb.id.asc())
    #         .order_by(
    #             AccouMdb.id.asc(),
    #             cast(func.replace(AccouMdb.acc_code, ".", ""), db.Integer).asc(),
    #         )
    #         .all()
    #     )
    #     data = [
    #         {
    #             "account": accou_schema.dump(x[0]),
    #             "kategory": kateg_schema.dump(x[1]),
    #             "klasifikasi": klasi_schema.dump(x[2]),
    #         }
    #         for x in result
    #     ]

    #     return response(200, "Berhasil", True, data)


@app.route("/v1/api/account/<int:page>/<int:length>/<string:filter>", methods=["GET"])
@token_required
def account_filter(self, page, length, filter):
    return AccountFilter(page, length, filter, request)


@app.route("/v1/api/import/account", methods=["POST"])
@token_required
def account_import(self):
    umum = request.json["umum"]
    detail = request.json["detail"]

    # db.session.query(AccouMdb).delete()
    db.session.execute('TRUNCATE TABLE master. "' +
                       "ACCOUMDB" + '" RESTART IDENTITY')
    db.session.commit()

    index_umum = 0
    index_detail = 0

    for x in umum:
        acc_name = x["acc_name"]
        umm_code = x["kode_umum"]
        kat_code = x["kode_kategori"]
        dou_type = x["du"]
        sld_type = x["kode_saldo"]
        connect = x["terhubung"]
        sld_awal = x["saldo_awal"]
        level = x["level"]

        index_umum += 1

        try:
            kategory = (
                db.session.query(KategMdb, KlasiMdb)
                .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                .order_by(KategMdb.id.asc())
                .filter(KategMdb.id == kat_code)
                .first()
            )

            key = str(kategory[1].id) + "." + str(kat_code)
            last_acc = (
                AccouMdb.query.filter(
                    and_(
                        AccouMdb.acc_code.like("%{}%".format(key)),
                        AccouMdb.dou_type == "U",
                    )
                )
                .order_by(AccouMdb.acc_code.desc())
                .first()
            )

            if last_acc != None:
                next_code = (
                    str(kategory[1].id)
                    + "."
                    + str(
                        int(last_acc.acc_code.replace(
                            str(kategory[1].id) + ".", ""))
                        + 1
                    )
                )
            else:
                next_code = str(kategory[1].id) + "." + str(kat_code) + "0001"

            a = AccouMdb(
                next_code,
                acc_name,
                umm_code,
                kat_code,
                dou_type,
                sld_type,
                connect,
                sld_awal,
                level,
            )
            db.session.add(a)
            db.session.commit()
            # print("UMUM ADDED")

        except IntegrityError:
            db.session.rollback()
            print("Err Umum %s" % (index_umum))

    for x in detail:
        acc_name = x["acc_name"]
        umm_code = x["kode_umum"]
        kat_code = x["kode_kategori"]
        dou_type = x["du"]
        sld_type = x["kode_saldo"]
        connect = x["terhubung"]
        sld_awal = x["saldo_awal"]

        index_detail += 1
        try:
            if umm_code:
                last_acc = (
                    AccouMdb.query.filter(AccouMdb.umm_code == umm_code)
                    .order_by(AccouMdb.acc_code.desc())
                    .first()
                )

                if last_acc != None:
                    next_code = (
                        umm_code
                        + "."
                        + str(int(last_acc.acc_code.replace(umm_code + ".", "")) + 1)
                    )
                else:
                    next_code = umm_code + "." + "1"
            else:
                kategory = (
                    db.session.query(KategMdb, KlasiMdb)
                    .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                    .order_by(KategMdb.id.asc())
                    .filter(KategMdb.id == kat_code)
                    .first()
                )

                key = str(kategory[1].id) + "." + str(kat_code)
                last_acc = (
                    AccouMdb.query.filter(
                        or_(
                            and_(
                                AccouMdb.acc_code.like("%{}%".format(key)),
                                AccouMdb.dou_type == "U",
                            ),
                            and_(
                                AccouMdb.acc_code.like("%{}%".format(key)),
                                AccouMdb.dou_type == "D",
                                AccouMdb.umm_code == None,
                            ),
                        )
                    )
                    .order_by(AccouMdb.acc_code.desc())
                    .first()
                )

                if last_acc:
                    next_code = (
                        str(kategory[1].id)
                        + "."
                        + str(
                            int(
                                last_acc.acc_code.replace(
                                    str(kategory[1].id) + ".", "")
                            )
                            + 1
                        )
                    )
                else:
                    next_code = str(kategory[1].id) + \
                        "." + str(kat_code) + "0001"

            a = AccouMdb(
                next_code,
                acc_name,
                umm_code,
                kat_code,
                dou_type,
                sld_type,
                connect,
                sld_awal,
                level,
            )
            db.session.add(a)
            db.session.commit()
            # print("Detail ADDED")

        except IntegrityError:
            db.session.rollback()
            print("Err Detail %s" % (index_detail))
            print(next_code)
            print(x)

    return response(200, "Berhasil", True, None)


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
    return AccountId(id, request)
    # account = AccouMdb.query.filter(AccouMdb.id == id).first()
    # if request.method == "PUT":
    #     account.acc_code = request.json["kode_acc"]
    #     account.acc_name = request.json["acc_name"]
    #     account.umm_code = request.json["kode_umum"]
    #     account.kat_code = request.json["kode_kategori"]
    #     account.dou_type = request.json["du"]
    #     account.sld_type = request.json["kode_saldo"]
    #     account.connect = request.json["terhubung"]
    #     account.sld_awal = request.json["saldo_awal"]
    #     account.level = request.json["level"]
    #     db.session.commit()

    #     return response(200, "Berhasil", True, accou_schema.dump(account))
    # elif request.method == "DELETE":
    #     db.session.delete(account)
    #     db.session.commit()

    #     return response(200, "Berhasil", True, None)
    # else:
    #     result = (
    #         db.session.query(AccouMdb, KategMdb, KlasiMdb)
    #         .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)
    #         .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
    #         .order_by(AccouMdb.acc_code.asc())
    #         .filter(AccouMdb.id == id)
    #         .first()
    #     )

    #     data = {
    #         "account": accou_schema.dump(result[0]),
    #         "kategory": kateg_schema.dump(result[1]),
    #         "klasifikasi": klasi_schema.dump(result[2]),
    #     }

    #     return response(200, "Berhasil", True, data)


@app.route("/v1/api/cost-center", methods=["POST", "GET"])
@token_required
def ccost(self):
    return CostCenter(request)


@app.route("/v1/api/cost-center/<int:page>/<int:length>/<string:filter>", methods=["GET"])
@token_required
def cost_center_filter(self, page, length, filter):
    return CcostFilter(page, length, filter)


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

            result = response(200, "Berhasil", True,
                              jpel_schema.dump(jenis_pel))
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
            result = response(200, "Berhasil", True,
                              jpel_schema.dump(jenis_pel))
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

            result = response(200, "Berhasil", True,
                              jpem_schema.dump(jenisPem))
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
            result = response(200, "Berhasil", True,
                              jpem_schema.dump(jenis_pem))
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

            result = response(200, "Berhasil", True,
                              sales_schema.dump(salesman))
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
            result = response(200, "Berhasil", True,
                              sales_schema.dump(salesman))
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
            area_pen = AreaPenjualanMdb(
                area_pen_code, area_pen_name, area_pen_ket)
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
    return Currency(self, request)


@app.route("/v1/api/currency/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def currency_id(self, id):
    return CurrencyId(id, self.company, request)


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

            result = response(200, "Berhasil", True,
                              rpay_schema.dump(rules_pay))
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
            result = response(200, "Berhasil", True,
                              rpay_schema.dump(rules_pay))
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
    file.save(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)
                            ), "static/upload", file_name
        )
    )

    return response(200, "Berhasil mengupload gambar", True, file_name)


@app.route("/v1/api/upload/<string:filename>", methods=["GET"])
def get_upload(filename):
    return send_from_directory("static/upload", filename)


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
            cutoff = request.json["cutoff"]
            year_co = request.json["year_co"]

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
                cutoff,
                year_co,
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
        result = CompMdb.query.filter(CompMdb.id == self.company).first()

        if result:
            result.cp_logo = result.cp_logo if result.cp_logo != "" else ""

        return response(200, "Berhasil", True, comp_shcema.dump(result))


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
            company.cutoff = request.json["cutoff"]
            company.year_co = request.json["year_co"]

            if server_name + "/v1/api/upload/" in request.json["cp_logo"]:
                cp_logo = request.json["cp_logo"].replace(
                    server_name + "/v1/api/upload/", ""
                )
            else:
                cp_logo = request.json["cp_logo"]

            if company.cp_logo != cp_logo:
                if company.cp_logo != "" and company.cp_logo is not None:
                    if os.path.exists(
                        os.path.join(
                            os.path.abspath(os.path.dirname(__file__)),
                            "static/upload",
                            company.cp_logo,
                        )
                    ):
                        os.remove(
                            os.path.join(
                                os.path.abspath(os.path.dirname(__file__)),
                                "static/upload",
                                company.cp_logo,
                            )
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
            company.cutoff = request.json["cutoff"]
            company.year_co = request.json["year_co"]

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
        cus_pkp = request.json["cus_pkp"]
        cus_country = request.json["cus_country"]
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
                cus_pkp,
                cus_country,
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
            result = response(200, "Berhasil", True,
                              customer_schema.dump(customer))
        except IntegrityError:
            db.session.rollback()
            return response(
                400, "Kode akun " + cus_code + " sudah digunakan", False, None
            )
        finally:
            return response(200, "Berhasil", True, customer_schema.dump(customer))
    else:
        result = (
            db.session.query(CustomerMdb, JpelMdb, SubAreaMdb,
                             CurrencyMdb, PajakMdb)
            .outerjoin(JpelMdb, JpelMdb.id == CustomerMdb.cus_jpel)
            .outerjoin(SubAreaMdb, SubAreaMdb.id == CustomerMdb.cus_sub_area)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == CustomerMdb.cus_curren)
            .outerjoin(PajakMdb, PajakMdb.id == CustomerMdb.cus_pjk)
            .order_by(JpelMdb.id.asc())
            # .order_by(CurrencyMdb.id.asc())
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
        customer.cus_pkp = request.json["cus_pkp"]
        customer.cus_country = request.json["cus_country"]
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
            db.session.query(CustomerMdb, JpelMdb, SubAreaMdb,
                             CurrencyMdb, PajakMdb)
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
        sup_pkp = request.json["sup_pkp"]
        sup_country = request.json["sup_country"]
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
                sup_pkp,
                sup_country,
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
            result = response(200, "Berhasil", True,
                              supplier_schema.dump(supplier))
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
        supplier.sup_pkp = request.json["sup_pkp"]
        supplier.sup_country = request.json["sup_country"]
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
            cp_id = self.company
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
            sls = request.json["sls"]
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
            sto_bb = request.json["sto_bb"]
            sto_bbp = request.json["sto_bbp"]
            fixed_assets = request.json["fixed_assets"]
            selisih_kurs = request.json["selisih_kurs"]

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
                sls,
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
                sto_bb,
                sto_bbp,
                fixed_assets,
                selisih_kurs,
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
        setup = SetupMdb.query.filter(SetupMdb.cp_id == self.company).first()
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
        setup.sls = request.json["sls"]
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
        setup.sto_bb = request.json["sto_bb"]
        setup.sto_bbp = request.json["sto_bbp"]
        setup.fixed_assets = request.json["fixed_assets"]
        setup.selisih_kurs = request.json["selisih_kurs"]
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


@app.route("/v1/api/setup/neraca", methods=["POST", "GET"])
@token_required
def setup_neraca(self):
    user = User.query.filter(User.id == self.id).first()
    if user is None:
        return response(404, "User not found", False, None)

    if request.method == "POST":
        try:
            cp_id = user.company
            tittle = request.json["tittle"]
            type = request.json["type"]
            accounts = request.json["accounts"]

            hdb = NeracaHdb(cp_id, tittle, type, self.id)

            db.session.add(hdb)
            db.session.commit()

            ddb = NeracaDdb(
                hdb.id,
                ",".join([str(x) for x in accounts]) if accounts else None,
                self.id,
            )

            db.session.add(ddb)
            db.session.commit()

            result = response(200, "Berhasil", True, None)
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        hdb = NeracaHdb.query.filter(NeracaHdb.cp_id == user.company).all()
        ddb = NeracaDdb.query.all()

        data = {"aktiva": [], "pasiva": []}
        if hdb:
            for x in hdb:
                for y in ddb:
                    if x.id == y.tittle_id:
                        if x.type == 1:
                            data["aktiva"].append(
                                {
                                    "id": x.id,
                                    "name": x.tittle,
                                    "category": y.accounts.replace("{", "")
                                    .replace("}", "")
                                    .split(",")
                                    if y.accounts
                                    else [None],
                                }
                            )
                        else:
                            data["pasiva"].append(
                                {
                                    "id": x.id,
                                    "name": x.tittle,
                                    "category": y.accounts.replace("{", "")
                                    .replace("}", "")
                                    .split(",")
                                    if y.accounts
                                    else [None],
                                }
                            )

            return response(200, "Berhasil", True, data)

        return response(200, "Berhasil", False, None)


@app.route("/v1/api/setup/neraca/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def setup_neraca_id(self, id):
    setup = NeracaMdb.query.filter(NeracaMdb.id == id).first()
    hdb = NeracaHdb.query.filter(NeracaHdb.id == id).first()
    if request.method == "PUT":
        ddb = NeracaDdb.query.filter(NeracaDdb.tittle_id == id).first()
        hdb.tittle = request.json["tittle"]
        if "accounts" in request.json:
            ddb.accounts = ",".join([str(x) for x in request.json["accounts"]])

        db.session.commit()

        return response(200, "Berhasil", True, None)
    elif request.method == "DELETE":
        db.session.delete(setup)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        if setup:
            setup.cur = (
                setup.cur.replace("{", "").replace("}", "").split(",")
                if setup.cur
                else None
            )
            setup.fixed = (
                setup.fixed.replace("{", "").replace("}", "").split(",")
                if setup.fixed
                else None
            )
            setup.depr = (
                setup.depr.replace("{", "").replace("}", "").split(",")
                if setup.depr
                else None
            )
            setup.ap = (
                setup.ap.replace("{", "").replace("}", "").split(",")
                if setup.ap
                else None
            )
            setup.cap = (
                setup.cap.replace("{", "").replace("}", "").split(",")
                if setup.cap
                else None
            )

            return response(200, "Berhasil", True, neraca_schema.dump(setup))

        return response(200, "Berhasil", False, None)


@app.route("/v1/api/setup/neraca-exep", methods=["POST", "GET"])
@token_required
def neraca_exep(self):
    user = User.query.filter(User.id == self.id).first()
    if request.method == "POST":
        try:
            accounts = request.json["accounts"]

            ddb = NeracaEceptionDdb(
                hdb.id,
                ",".join([str(x) for x in accounts]) if accounts else None,
                self.id,
            )

            db.session.add(ddb)
            db.session.commit()

            result = response(200, "Berhasil", True, None)
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        hdb = NeracaHdb.query.filter(NeracaHdb.cp_id == user.company).all()
        ddb = NeracaEceptionDdb.query.all()

        final = []
        if ddb:
            for x in hdb:
                for y in ddb:
                    final.append(
                        {
                            "id": x.id,
                            "title_id": x.tittle,
                            "accounts": y.accounts.replace("{", "")
                            .replace("}", "")
                            .split(",")
                            if y.accounts
                            else [None],
                        }
                    )

            return response(200, "Berhasil", True, final)

        return response(200, "Berhasil", False, None)


@app.route("/v1/api/setup/pnl", methods=["POST", "GET"])
@token_required
def setup_pnl(self):
    user = User.query.filter(User.id == self.id).first()
    if request.method == "POST":
        try:
            cp_id = user.company
            klasi = request.json["klasi"]

            setup = PnlMdb(
                cp_id,
                ",".join([str(x) for x in klasi]) if klasi else None,
                self.id,
            )

            db.session.add(setup)
            db.session.commit()

            result = response(200, "Berhasil", True, pnl_schema.dump(setup))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        setup = PnlMdb.query.filter(PnlMdb.cp_id == self.company).first()

        if setup:
            setup.klasi = (
                setup.klasi.replace("{", "").replace("}", "").split(",")
                if setup.klasi
                else None
            )

            return response(200, "Berhasil", True, pnl_schema.dump(setup))

        return response(200, "Berhasil", False, None)


@app.route("/v1/api/setup/pnl/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def setup_pnl_id(self, id):
    setup = PnlMdb.query.filter(PnlMdb.id == id).first()
    if request.method == "PUT":
        setup.klasi = request.json["klasi"]

        db.session.commit()

        return response(200, "Berhasil", True, neraca_schema.dump(setup))
    elif request.method == "DELETE":
        db.session.delete(setup)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        if setup:
            setup.klasi = (
                setup.klasi.replace("{", "").replace("}", "").split(",")
                if setup.klasi
                else None
            )

            return response(200, "Berhasil", True, pnl_schema.dump(setup))

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
                    result = response(200, "Berhasil", True,
                                      units_schema.dump(u))
                else:
                    u = UnitMdb(code, name, type, desc,
                                active, qty, u_from, u_to)
                    db.session.add(u)
                    db.session.commit()
                    result = response(200, "Berhasil", True,
                                      unit_schema.dump(u))
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
                        x.u_from = UnitSchema(
                            only=["id", "code", "name"]).dump(y)
            if x.type == "k" and x.u_to:
                for y in units:
                    if x.u_to == y.id:
                        x.u_to = UnitSchema(
                            only=["id", "code", "name"]).dump(y)

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
                    db.session.query(UnitMdb).filter(
                        UnitMdb.id.in_(old_ids)).all()
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


@app.route("/v1/api/product/code", methods=["POST", "GET"])
@token_required
def product_code(self):
    now = datetime.now().strftime("%d%m%y")
    prd = "PRD/" + now + "/" + str(round(time.time() * 10000))[-6:]
    return response(200, "success", True, prd)


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
            weight = request.json["weight"]
            dm_panjang = request.json["dm_panjang"]
            dm_lebar = request.json["dm_lebar"]
            dm_tinggi = request.json["dm_tinggi"]
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
            ns = request.json["ns"]
            ket = request.json["ket"]
            suplier = request.json["suplier"]

            prod = ProdMdb(
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
                None,
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
                False,
            )
            db.session.add(prod)
            db.session.commit()

            new_supp = []
            for x in suplier:
                if prod.id:
                    new_supp.append(ProdSupMdb(prod.id, x["sup_id"]))

            if len(new_supp) > 0:
                db.session.add_all(new_supp)

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            return response(400, "Kode sudah digunakan", False, None)
        finally:
            return response(200, "Berhasil", True, prod_schema.dump(prod))
    else:
        try:
            result = (
                db.session.query(ProdMdb, UnitMdb, GroupProMdb)
                .outerjoin(UnitMdb, UnitMdb.id == ProdMdb.unit)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .order_by(ProdMdb.id.asc())
                .all()
            )

            sup = (
                db.session.query(ProdSupDdb, SupplierMdb)
                .outerjoin(SupplierMdb, SupplierMdb.id == ProdSupDdb.sup_id)
                .order_by(ProdSupDdb.id.asc())
                .all()
            )

            data = []

            if result:
                for x in result:
                    supp = []
                    for y in sup:
                        if x[0].id == y[0].prod_id:
                            y[0].sup_id = supplier_schema.dump(
                                y[1]) if y[1] else None
                            sup.append(prodsup_schema.dump(y[0]))

                    # x[0].image = (
                    #     request.host_url + "static/upload/" + x[0].image
                    #     if x[0].image and x[0].image != ""
                    #     else None
                    # )

                    data.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "name": x[0].name,
                            "group": groupPro_schema.dump(
                                x[2]) if x[2] else None,
                            "type": x[0].type,
                            "codeb": x[0].codeb,
                            "unit": unit_schema.dump(x[1]) if x[1] else None,
                            "weight": x[0].weight,
                            "dm_panjang": x[0].dm_panjang,
                            "dm_lebar": x[0].dm_lebar,
                            "dm_tinggi": x[0].dm_tinggi,
                            "s_price": x[0].s_price,
                            "barcode": x[0].barcode,
                            "metode": x[0].metode,
                            "max_stock": x[0].max_stock,
                            "min_stock": x[0].min_stock,
                            "re_stock": x[0].re_stock,
                            "lt_stock": x[0].lt_stock,
                            "max_order": x[0].max_order,
                            "ns": x[0].ns,
                            "ket": x[0].ket,
                            "image": request.host_url + "static/upload/" + x[0].image
                            if x[0].image and x[0].image != ""
                            else None,
                            "suplier": supp,
                        }
                    )

            return response(200, "Berhasil", True, data)
        except ProgrammingError as e:
            print(e)
            return UpdateTable([ProdMdb, ProdSupDdb], request)


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
            prod.weight = request.json["weight"]
            prod.dm_panjang = request.json["dm_panjang"]
            prod.dm_lebar = request.json["dm_lebar"]
            prod.dm_tinggi = request.json["dm_tinggi"]
            prod.b_price = request.json["b_price"]
            prod.s_price = request.json["s_price"]
            prod.barcode = request.json["barcode"]
            prod.metode = request.json["metode"]
            prod.max_stock = request.json["max_stock"]
            prod.min_stock = request.json["min_stock"]
            prod.re_stock = request.json["re_stock"]
            prod.lt_stock = request.json["lt_stock"]
            prod.max_order = request.json["max_order"]
            prod.ns = request.json["ns"]
            prod.ket = request.json["ket"]
            prod.suplier = request.json["suplier"]

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
                        os.remove(os.path.join(
                            app.config["UPLOAD_FOLDER"], prod.image))

            prod.image = image

            db.session.commit()

            sup = ProdSupDdb.query.filter(ProdSupDdb.prod_id == prod.id).all()

            old_sup = []
            new_sup = []
            for x in suplier:
                if x["id"] != 0:
                    old_sup.append(x["id"])
                else:
                    new_sup.append(
                        ProdSupDdb(
                            x.id,
                            x["sup_id"],
                        )
                    )

            if len(old_sup) > 0:
                for x in old_sup:
                    for y in sup:
                        if y.id not in old_sup:
                            db.session.delete(y)
                        else:
                            if y.id == x:
                                for z in suplier:
                                    if z["id"] == x:
                                        y.su_id = z["su_id"]

            if len(new_sup) > 0:
                db.session.add_all(new_sup)

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


@app.route("/v1/api/import/prod", methods=["POST"])
@token_required
def prod_import(self):

    prod = request.json["prod"]

    if ProdMdb.imp == True:
        db.session.query(ProdMdb).delete()
        db.session.commit()

    a = []
    for x in prod:
        code = x["code"]
        name = x["name"]
        group = x["group"]
        unit = x["unit"]
        metode = x["metode"]
        ns = False
        a.append(
            ProdMdb(
                code,
                name,
                group,
                None,
                None,
                unit,
                None,
                None,
                None,
                None,
                metode,
                None,
                None,
                None,
                None,
                None,
                ns,
                None,
                True,
                True,
            )
        )

    try:
        db.session.execute(
            'TRUNCATE TABLE master. "' + "PRODMDB" + '" RESTART IDENTITY'
        )
        db.session.commit()

        db.session.add_all(a)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

    return response(200, "Berhasil", True, None)


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

            result = response(200, "Berhasil", True,
                              division_schema.dump(divisi))
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
            result = response(200, "Berhasil", True,
                              division_schema.dump(divisi))
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
    return GroupProduct(self, request)


@app.route("/v1/api/group-product/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def groupPro_id(self, id):
    return GroupProductId(id, request)


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
    return RequestPurchase(self, request)


@app.route("/v1/api/rp/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def rp_id(self, id):
    return RequestPurchaseId(id, request)


@app.route("/v1/api/po", methods=["POST", "GET"])
@token_required
def po(self):
    return PurchaseOrder(self, request)


@app.route("/v1/api/po/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def po_id(self, id):
    return PurchaseOrderId(id, request)


@app.route("/v1/api/po-close/<int:id>", methods=["PUT"])
@token_required
def po_close_id(self, id):
    return PurchaseOrderClose(id, request)


@app.route("/v1/api/so", methods=["POST", "GET"])
@token_required
def so(self):
    return SalesOrder(self, request)


@app.route("/v1/api/so/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def so_id(self, id):
    return SalesOrderId(id, request)


@app.route("/v1/api/so-close/<int:id>", methods=["PUT"])
@token_required
def so_close_id(self, id):
    return SalesOrderClose(id, request)


@app.route("/v1/api/order", methods=["POST", "GET"])
@token_required
def order(self):
    return Order(self, request)


@app.route("/v1/api/order/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def ord_id(self, id):
    return OrderId(id, request)


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
                y[0].location = loct_schema.dump(
                    y[3]) if y[0].location else None
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


@app.route("/v1/api/invoice-pb", methods=["POST", "GET"])
@token_required
def invoice_pb(self):
    return InvoicePb(self, request)


@app.route("/v1/api/invoice-pb/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def invoice_pb_id(self, id):
    return InvoicePbId(id, request)


@app.route("/v1/api/faktur-pb", methods=["POST", "GET"])
@token_required
def faktur(self):
    return FakturPb(self, request)


@app.route("/v1/api/faktur-pb/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def faktur_id(self, id):
    return FakturPbId(id, request)


@app.route("/v1/api/retur-order", methods=["POST", "GET"])
@token_required
def retur_order(self):
    return ReturOrder(self, request)


@app.route("/v1/api/retur-order/<int:id>", methods=["PUT", "DELETE", "GET"])
@token_required
def retur_order_id(self, id):
    return ReturOrderId(id, request)


@app.route("/v1/api/retur-sales", methods=["POST", "GET"])
@token_required
def retur_sales(self):
    return ReturSale(self, request)


@app.route("/v1/api/retur-sales/<int:id>", methods=["PUT", "DELETE", "GET"])
@token_required
def retur_sale_id(self, id):
    return ReturSaleId(id, request)


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
    return Sale(self, request)


@app.route("/v1/api/sales/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def sls_id(self, id):
    return SaleId(id, request)


@app.route("/v1/api/invoice-pj", methods=["POST", "GET"])
@token_required
def invoice_pj(self):
    return InvoicePj(self, request)


@app.route("/v1/api/invoice-pj/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def invoice_pj_id(self, id):
    return InvoicePjId(id, request)


@app.route("/v1/api/faktur-pj", methods=["POST", "GET"])
@token_required
def faktur_pj(self):
    return FakturPj(self, request)


@app.route("/v1/api/faktur-pj/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def faktur_pj_id(self, id):
    return FakturPjId(id, request)


@app.route("/v1/api/expense", methods=["POST", "GET"])
@token_required
def expense(self):
    return Expense(self, request)


@app.route("/v1/api/expense/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def expense_id(self, id):
    return ExpenseId(id, request)


@app.route("/v1/api/income", methods=["POST", "GET"])
@token_required
def income(self):
    return Income(self, request)


@app.route("/v1/api/income/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def income_id(self, id):
    return IncomeId(id, request)


@app.route("/v1/api/apcard", methods=["GET"])
@token_required
def apcard(self):
    ap = (
        db.session.query(ApCard, AcqDdb, PoMdb, SupplierMdb, OrdpbHdb, GiroHdb)
        .outerjoin(AcqDdb, AcqDdb.id == ApCard.acq_id)
        .outerjoin(PoMdb, PoMdb.id == ApCard.po_id)
        .outerjoin(SupplierMdb, SupplierMdb.id == ApCard.sup_id)
        .outerjoin(OrdpbHdb, OrdpbHdb.id == ApCard.ord_id)
        .outerjoin(GiroHdb, GiroHdb.id == ApCard.giro_id)
        .all()
    )

    final = []
    for x in ap:
        final.append(
            {
                "id": x[0].id,
                "trx_code": x[0].trx_code,
                "sup_id": supplier_schema.dump(x[3]) if x[3] else None,
                # "fk_id": fkpb_schema.dump(x[6]) if x[6] else None,
                "ord_id": dord_schema.dump(x[4]) if x[4] else None,
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
                "sa_id": x[0].sa_id,
                "sa": x[0].sa,
                "lunas": x[0].lunas,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/arcard", methods=["GET"])
@token_required
def arcard(self):
    ar = (
        db.session.query(ArCard, IAcqDdb, OrdpjHdb,
                         CustomerMdb, SordHdb, GiroIncHdb)
        .outerjoin(IAcqDdb, IAcqDdb.id == ArCard.acq_id)
        .outerjoin(OrdpjHdb, OrdpjHdb.id == ArCard.bkt_id)
        .outerjoin(CustomerMdb, CustomerMdb.id == ArCard.cus_id)
        .outerjoin(SordHdb, SordHdb.id == ArCard.so_id)
        .outerjoin(GiroIncHdb, GiroIncHdb.id == ArCard.giro_id)
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
                "acq_id": iacq_schema.dump(x[1]) if x[1] else None,
                "acq_date": ARCardSchema(only=["acq_date"]).dump(x[0])["acq_date"]
                if x[0]
                else None,
                "bkt_id": ordpj_schema.dump(x[2]) if x[2] else None,
                "bkt_date": OrdpjSchema(only=["ord_date"]).dump(x[2])["ord_date"]
                if x[2]
                else None,
                "cur_conv": x[0].cur_conv,
                "trx_dbcr": x[0].trx_dbcr,
                "trx_type": x[0].trx_type,
                "pay_type": x[0].pay_type,
                "trx_amnh": x[0].trx_amnh,
                "trx_amnv": x[0].trx_amnv,
                "acq_amnh": x[0].acq_amnh,
                "acq_amnv": x[0].acq_amnv,
                "bkt_amnv": x[0].bkt_amnv,
                "bkt_amnh": x[0].bkt_amnh,
                "trx_desc": x[0].trx_desc,
                "pos_flag": x[0].pos_flag,
                "giro_id": grinc_schema.dump(x[5]) if x[5] else None,
                "giro_date": GiroIncSchema(only=["giro_date"]).dump(x[5])["giro_date"]
                if x[5]
                else None,
                "so_id": sord_schema.dump(x[4]) if x[4] else None,
                "trx_pymnt": x[0].trx_pymnt,
                "sa_id": x[0].sa_id,
                "sa": x[0].sa,
                "lunas": x[0].lunas,
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
        db.session.query(extract("month", ApCard.ord_date),
                         func.sum(ApCard.trx_amnh))
        .filter(and_(ApCard.trx_type == "LP", ApCard.pay_type == "P1"))
        .group_by(extract("month", ApCard.ord_date))
        .all()
    )
    ar = (
        db.session.query(extract("month", ArCard.trx_date),
                         func.sum(ArCard.trx_amnh))
        .filter(and_(ArCard.trx_type == "JL", ArCard.pay_type == "P1"))
        .group_by(extract("month", ArCard.trx_date))
        .all()
    )

    lns_ap = (
        db.session.query(extract("month", ApCard.ord_date),
                         func.sum(ApCard.acq_amnh))
        .filter(and_(ApCard.trx_type == "LP", ApCard.pay_type == "H4"))
        .group_by(extract("month", ApCard.ord_date))
        .all()
    )
    lns_ar = (
        db.session.query(extract("month", ArCard.trx_date),
                         func.sum(ArCard.acq_amnh))
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
            giro.status = 1

            db.session.commit()

            result = response(200, "Berhasil", True, giro_schema.dump(giro))

        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    # elif request.method == "DELETE":
    #     db.session.delete(giro)
    #     db.session.commit()

    #     return response(200, "Berhasil", True, None)
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


@app.route("/v1/api/giro-inc", methods=["GET"])
@token_required
def giro_inc(self):
    giro = (
        db.session.query(GiroIncHdb, BankMdb, CustomerMdb, IncHdb)
        .outerjoin(BankMdb, BankMdb.id == GiroIncHdb.bank_id)
        .outerjoin(CustomerMdb, CustomerMdb.id == GiroIncHdb.cus_id)
        .outerjoin(IncHdb, IncHdb.id == GiroIncHdb.pay_code)
        .all()
    )

    final = []
    for x in giro:
        final.append(
            {
                "id": x[0].id,
                "giro_date": GiroIncSchema(only=["giro_date"]).dump(x[0])["giro_date"]
                if x[0]
                else None,
                "giro_num": x[0].giro_num,
                "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                "pay_code": inc_schema.dump(x[3]) if x[3] else None,
                "pay_date": GiroIncSchema(only=["pay_date"]).dump(x[0])["pay_date"]
                if x[0]
                else None,
                "cus_id": customer_schema.dump(x[2]) if x[2] else None,
                "value": x[0].value,
                "accp_date": GiroIncSchema(only=["accp_date"]).dump(x[0])["accp_date"]
                if x[0]
                else None,
                "status": x[0].status,
            }
        )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/giro-inc/<int:id>", methods=["PUT", "GET"])
@token_required
def giro_inc_id(self, id):
    gr = GiroIncHdb.query.filter(GiroIncHdb.id == id).first()
    if request.method == "PUT":
        try:
            gr.giro_date = request.json["giro_date"]
            gr.giro_num = request.json["giro_num"]
            gr.bank_id = request.json["bank_id"]
            gr.pay_code = request.json["pay_code"]
            gr.pay_date = request.json["pay_date"]
            gr.cus_id = request.json["cus_id"]
            gr.value = request.json["value"]
            gr.status = 1

            db.session.commit()

            UpdateArGiro(gr.id)

            result = response(200, "Berhasil", True, grinc_schema.dump(gr))

        # except IntegrityError:
        #     db.session.rollback()
        #     result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result

    else:
        gir = (
            db.session.query(GiroIncHdb, BankMdb, CustomerMdb, IncHdb)
            .outerjoin(BankMdb, BankMdb.id == GiroIncHdb.bank_id)
            .outerjoin(CustomerMdb, CustomerMdb.id == GiroIncHdb.cus_id)
            .outerjoin(IncHdb, IncHdb.id == GiroIncHdb.pay_code)
            .all()
        )

        final = []
        for x in gir:

            if x[0].pay_code:
                if x[3].id == x[0].pay_code:
                    x[0].pay_code = inc_schema.dump(x[3])

            final.append(
                {
                    "id": x[0].id,
                    "giro_date": GiroIncSchema(only=["giro_date"]).dump(x[0])[
                        "giro_date"
                    ]
                    if x[0]
                    else None,
                    "giro_num": x[0].giro_num,
                    "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                    "pay_code": inc_schema.dump(x[3]) if x[3] else None,
                    "pay_date": GiroIncSchema(only=["pay_date"]).dump(x[0])["pay_date"]
                    if x[0]
                    else None,
                    "cus_id": customer_schema.dump(x[2]) if x[2] else None,
                    "value": x[0].value,
                    "accp_date": GiroIncSchema(only=["accp_date"]).dump(x[0])[
                        "accp_date"
                    ]
                    if x[0]
                    else None,
                    "status": x[0].status,
                }
            )

        return response(200, "Berhasil", True, final)


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
    return Formula(self, request)


@app.route("/v1/api/formula/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def formula_id(self, id):
    return FormulaId(self, id, request)


@app.route("/v1/api/planning", methods=["GET", "POST"])
@token_required
def planning(self):
    return Planning(self, request)


@app.route("/v1/api/planning/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def planning_id(self, id):
    return PlanningId(id, request)


@app.route("/v1/api/batch", methods=["GET", "POST"])
@token_required
def batch(self):
    return Batch(self, request)


@app.route("/v1/api/batch/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def batch_id(self, id):
    return BatchId(id, request)


@app.route("/v1/api/phj", methods=["GET", "POST"])
@token_required
def phj(self):
    return PenerimaanHasilJadi(self, request)


@app.route("/v1/api/phj/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def phj_id(self, id):
    return PenerimaanHasilJadiId(id, request)


@app.route("/v1/api/pbb", methods=["GET", "POST"])
@token_required
def pbb(self):
    return Pembebanan(self, request)


@app.route("/v1/api/pbb/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def pbb_id(self, id):
    return PembebananId(id, request)


@app.route("/v1/api/rpbb", methods=["GET"])
@token_required
def rpbb(self):
    rpbb = (
        db.session.query(RpbbMdb, PlanHdb, FprdcHdb, ProdMdb, LocationMdb)
        .outerjoin(PlanHdb, PlanHdb.id == RpbbMdb.pl_id)
        .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
        .outerjoin(ProdMdb, ProdMdb.id == RpbbMdb.prod_id)
        .outerjoin(LocationMdb, LocationMdb.id == RpbbMdb.loc_id)
        .all()
    )

    final = []
    for x in rpbb:
        x[1].form_id = fprdc_schema.dump(x[2])
        x[0].pl_id = plan_schema.dump(x[1])
        x[0].prod_id = prod_schema.dump(x[3])
        x[0].loc_id = loct_schema.dump(x[4])
        final.append(rpbb_schema.dump(x[0]))

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/apprv-bnk", methods=["GET"])
@token_required
def approve_bank(self):
    company = (
        db.session.query(User, CompMdb)
        .outerjoin(CompMdb, User.company == CompMdb.id)
        .filter(User.id == self.id)
        .first()
    )

    exps = (
        db.session.query(ExpHdb, BankMdb, SupplierMdb, CcostMdb, ProjMdb)
        .outerjoin(BankMdb, BankMdb.id == ExpHdb.bank_id)
        .outerjoin(SupplierMdb, SupplierMdb.id == ExpHdb.acq_sup)
        .outerjoin(CcostMdb, CcostMdb.id == ExpHdb.exp_dep)
        .outerjoin(ProjMdb, ProjMdb.id == ExpHdb.exp_prj)
        .filter(ExpHdb.approve == False)
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
    if company and company[1].appr_payment:
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
                    "exp_dep": ccost_schema.dump(x[3]) if x[3] else None,
                    "exp_prj": proj_schema.dump(x[4]) if x[4] else None,
                    "acq_sup": supplier_schema.dump(x[2]) if x[2] else None,
                    "acq_pay": x[0].acq_pay,
                    "kas_acc": x[0].kas_acc,
                    "bank_acc": x[0].bank_acc,
                    "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                    "bank_ref": x[0].bank_ref,
                    "giro_num": x[0].giro_num,
                    "giro_date": ExpSchema(only=["giro_date"]).dump(x[0])["giro_date"],
                    "approve": x[0].approve,
                    "exp": all_exp,
                    "acq": all_acq,
                }
            )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/apprv-bnk/<int:id>", methods=["GET"])
@token_required
def approve_bank_id(self, id):
    exps = ExpHdb.query.filter(ExpHdb.id == id).first()

    acq = (
        db.session.query(AcqDdb, FkpbHdb)
        .outerjoin(FkpbHdb, FkpbHdb.id == AcqDdb.fk_id)
        .all()
    )
    if exps:
        value = 0
        for x in acq:
            if x[0].exp_id == exps.id:
                value += x[0].payment

        if exps.acq_pay == 3:
            giro = GiroHdb(
                exps.giro_date,
                exps.giro_num,
                exps.bank_id,
                exps.id,
                exps.exp_date,
                exps.acq_sup,
                value,
                0,
            )
            db.session.add(giro)
            db.session.commit()
            UpdateApGiro(giro.id)

        # if exps.acq_pay != 3:
        UpdateApPayment(exps.id, False)

        exps.approve = True

        db.session.commit()
    return response(200, "Berhasil", True, None)


@app.route("/v1/api/memorial", methods=["GET", "POST"])
@token_required
def memorial(self):
    if request.method == "POST":
        try:
            code = request.json["code"]
            date = request.json["date"]
            desc = request.json["desc"]
            memo = request.json["memo"]

            m = MemoHdb(code, date, desc, False, False, self.id)

            db.session.add(m)
            db.session.commit()

            print(memo)
            new_memo = []
            for x in memo:
                if x["acc_id"] and x["dbcr"] and x["amnt"]:
                    new_memo.append(
                        MemoDdb(
                            m.id,
                            x["acc_id"],
                            x["dep_id"],
                            x["currency"],
                            x["dbcr"],
                            x["amnt"],
                            x["amnh"],
                            x["desc"],
                        )
                    )

            print(len(new_memo))
            if len(new_memo) > 0:
                db.session.add_all(new_memo)
                db.session.commit()

                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == m.code).all()
                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)
                        db.session.commit()

                all_trans = []
                for x in new_memo:
                    all_trans.append(
                        TransDdb(
                            m.code,
                            m.date,
                            x.acc_id,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            x.amnt,
                            "D" if x.dbcr == "d" else "K",
                            "JURNAL MEMORIAL %s" % (m.code),
                            None,
                            None,
                        )
                    )

                    if len(all_trans) > 0:
                        db.session.add_all(all_trans)
                        db.session.commit()

            result = response(200, "Berhasil", True, mhdb_schema.dump(m))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        m = MemoHdb.query.order_by(MemoHdb.id.desc()).all()

        memo = (
            db.session.query(MemoDdb, AccouMdb, CcostMdb, CurrencyMdb)
            .outerjoin(AccouMdb, AccouMdb.id == MemoDdb.acc_id)
            .outerjoin(CcostMdb, CcostMdb.id == MemoDdb.dep_id)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == MemoDdb.currency)
            .all()
        )

        final = []
        for x in m:
            mm = []
            for y in memo:
                if x.id == y[0].mcode:
                    y[0].acc_id = accou_schema.dump(y[1])
                    y[0].dep_id = ccost_schema.dump(y[2])
                    y[0].currency = currency_schema.dump(
                        y[3]) if y[3] else None
                    mm.append(mddb_schema.dump(y[0]))

            final.append(
                {
                    "id": x.id,
                    "code": x.code,
                    "date": MhdbSchema(only=["date"]).dump(x)["date"],
                    "desc": x.desc,
                    "imp": x.imp,
                    "closing": x.closing,
                    "memo": mm,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/memorial/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def memorial_id(self, id):
    x = MemoHdb.query.filter(MemoHdb.id == id).first()
    if request.method == "PUT":
        try:
            code = request.json["code"]
            date = request.json["date"]
            desc = request.json["desc"]
            memo = request.json["memo"]

            x.code = code
            x.date = date
            x.desc = desc

            db.session.commit()

            old_memo = MemoDdb.query.filter(MemoDdb.mcode == id).all()
            new_memo = []
            for y in old_memo:
                for z in memo:
                    if z["id"]:
                        if z["id"] == y.id:
                            if z["id"] and z["acc_id"] and z["dbcr"] and z["amnt"]:
                                y.acc_id = z["acc_id"]
                                y.dep_id = z["dep_id"]
                                y.currency = z["currency"]
                                y.dbcr = z["dbcr"]
                                y.amnt = z["amnt"]
                                y.amnh = z["amnh"]
                                y.desc = z["desc"]

                    else:

                        if z["acc_id"] and z["dbcr"] and z["amnt"]:
                            new_memo.append(
                                MemoDdb(
                                    x.id,
                                    z["acc_id"],
                                    z["dep_id"],
                                    z["currency"],
                                    z["dbcr"],
                                    z["amnt"],
                                    z["amnh"],
                                    z["desc"],
                                )
                            )

            if len(new_memo) > 0:
                db.session.add_all(new_memo)

            db.session.commit()

            new_memo = MemoDdb.query.filter(MemoDdb.mcode == id).all()
            old_trans = TransDdb.query.filter(
                TransDdb.trx_code == x.code).all()
            if old_trans:
                for y in old_trans:
                    db.session.delete(y)
                    db.session.commit()

            all_trans = []
            for y in new_memo:
                all_trans.append(
                    TransDdb(
                        x.code,
                        x.date,
                        y.acc_id,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        y.amnt,
                        "D" if y.dbcr == "d" else "K",
                        "JURNAL MEMORIAL %s" % (x.code),
                        None,
                        None,
                    )
                )

            if len(all_trans) > 0:
                db.session.add_all(all_trans)
                db.session.commit()

            result = response(200, "Berhasil", True, mhdb_schema.dump(x))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    elif request.method == "DELETE":
        old_trans = TransDdb.query.filter(TransDdb.trx_code == x.code).all()
        if old_trans:
            for y in old_trans:
                db.session.delete(y)
                db.session.commit()
        old_memo = MemoDdb.query.filter(MemoDdb.mcode == id).all()

        if old_memo:
            for y in old_memo:
                db.session.delete(y)

        db.session.delete(x)
        db.session.commit()

        return response(200, "Berhasil", True, None)
    else:
        memo = (
            db.session.query(MemoDdb, AccouMdb, CcostMdb, CurrencyMdb)
            .outerjoin(AccouMdb, AccouMdb.id == MemoDdb.acc_id)
            .outerjoin(CcostMdb, CcostMdb.id == MemoDdb.dep_id)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == MemoDdb.currency)
            .all()
        )

        mm = []
        for y in memo:
            if x.id == y[0].mcode:
                y[0].acc_id = accou_schema.dump(y[1])
                y[0].dep_id = ccost_schema.dump(y[2])
                y[0].currency = currency_schema.dump(y[3]) if y[3] else None
                mm.append(mddb_schema.dump(y[0]))

        final = {
            "id": x.id,
            "code": x.code,
            "date": MhdbSchema(only=["date"]).dump(x)["date"],
            "desc": x.desc,
            "memo": mm,
        }

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/import/memorial", methods=["POST"])
@token_required
def memo_import(self):
    mem = request.json["memo"]

    for x in mem:
        try:
            code = x["code"]
            date = x["date"]
            desc = x["desc"]
            memo = x["memo"]

            m = MemoHdb(code, date, desc, True, False, self.id)

            db.session.add(m)
            db.session.commit()

            print(memo)
            new_memo = []
            for x in memo:
                if x["acc_id"] and x["dbcr"] and x["amnt"]:
                    new_memo.append(
                        MemoDdb(
                            m.id,
                            x["acc_id"],
                            x["dep_id"],
                            x["currency"],
                            x["dbcr"],
                            x["amnt"],
                            x["amnh"],
                            x["desc"],
                        )
                    )

            print(len(new_memo))
            if len(new_memo) > 0:
                db.session.add_all(new_memo)
                db.session.commit()

                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == m.code).all()
                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)
                        db.session.commit()

                all_trans = []
                for x in new_memo:
                    all_trans.append(
                        TransDdb(
                            m.code,
                            m.date,
                            x.acc_id,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            x.amnt,
                            "D" if x.dbcr == "d" else "K",
                            "JURNAL MEMORIAL %s" % (m.code),
                            None,
                            None,
                        )
                    )

                    if len(all_trans) > 0:
                        db.session.add_all(all_trans)
                        db.session.commit()

        except IntegrityError:
            db.session.rollback()

    return response(200, "Berhasil", True, None)


@app.route("/v1/api/mutasi", methods=["GET", "POST"])
@token_required
def mutasi(self):
    if request.method == "POST":
        try:
            mtsi_code = request.json["mtsi_code"]
            mtsi_date = request.json["mtsi_date"]
            loc_from = request.json["loc_from"]
            loc_to = request.json["loc_to"]
            dep_id = request.json["dep_id"]
            prj_id = request.json["prj_id"]
            doc = request.json["doc"]
            doc_date = request.json["doc_date"]
            mutasi = request.json["mutasi"]

            mt = MtsiHdb(
                mtsi_code, mtsi_date, loc_from, loc_to, dep_id, prj_id, doc, doc_date
            )

            db.session.add(mt)
            db.session.commit()

            new_mutasi = []
            for x in mutasi:
                if x["prod_id"] and x["qty"] and x["unit_id"]:
                    new_mutasi.append(
                        MtsiDdb(
                            mt.id,
                            x["prod_id"],
                            x["unit_id"],
                            x["qty"],
                        )
                    )

            if len(new_mutasi) > 0:
                db.session.add_all(new_mutasi)
                db.session.commit()

            UpdateMutasi(mt.id, False)

            result = response(200, "Berhasil", True, mtsi_schema.dump(mt))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        mt = (
            db.session.query(MtsiHdb, CcostMdb, ProjMdb)
            .outerjoin(CcostMdb, CcostMdb.id == MtsiHdb.dep_id)
            .outerjoin(ProjMdb, ProjMdb.id == MtsiHdb.prj_id)
            .order_by(MtsiHdb.id.desc())
            .all()
        )

        mts = (
            db.session.query(MtsiDdb, ProdMdb, UnitMdb)
            .outerjoin(ProdMdb, ProdMdb.id == MtsiDdb.prod_id)
            .outerjoin(UnitMdb, UnitMdb.id == MtsiDdb.unit_id)
            .all()
        )

        loc = LocationMdb.query.all()

        final = []
        for x in mt:
            mut = []
            for y in mts:
                if x[0].id == y[0].mtsi_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    mut.append(mtsiddb_schema.dump(y[0]))

            for y in loc:
                if x[0].loc_from == y.id:
                    x[0].loc_from = loct_schema.dump(y)

                if x[0].loc_to == y.id:
                    x[0].loc_to = loct_schema.dump(y)

            final.append(
                {
                    "id": x[0].id,
                    "mtsi_code": x[0].mtsi_code,
                    "mtsi_date": MtsiSchema(only=["mtsi_date"]).dump(x[0])["mtsi_date"],
                    "loc_from": x[0].loc_from,
                    "loc_to": x[0].loc_to,
                    "dep_id": ccost_schema.dump(x[1]) if x[1] else None,
                    "prj_id": proj_schema.dump(x[2]) if x[2] else None,
                    "doc": x[0].doc,
                    "doc_date": MtsiSchema(only=["doc_date"]).dump(x[0])["doc_date"],
                    "mutasi": mut,
                }
            )

        return response(200, "Berhasil", True, final)


@app.route("/v1/api/mutasi/<int:id>", methods=["PUT", "DELETE"])
@token_required
def mutasi_id(self, id):
    x = MtsiHdb.query.filter(MtsiHdb.id == id).first()
    if request.method == "PUT":
        try:
            mtsi_code = request.json["mtsi_code"]
            mtsi_date = request.json["mtsi_date"]
            loc_from = request.json["loc_from"]
            loc_to = request.json["loc_to"]
            dep_id = request.json["dep_id"]
            prj_id = request.json["prj_id"]
            doc = request.json["doc"]
            doc_date = request.json["doc_date"]
            mt = request.json["mutasi"]

            x.mtsi_code = mtsi_code
            x.mtsi_date = mtsi_date
            x.loc_from = loc_from
            x.loc_to = loc_to
            x.dep_id = dep_id
            x.prj_id = prj_id
            x.doc = doc
            x.doc_date = doc_date

            db.session.commit()

            old_mutasi = MtsiDdb.query.filter(MtsiDdb.mtsi_id == id).all()
            new_mutasi = []
            for z in mt:
                if z["id"]:
                    for y in old_mutasi:
                        if z["id"] == y.id:
                            if z["id"] and z["prod_id"] and z["qty"] and z["unit_id"]:
                                y.prod_id = z["prod_id"]
                                y.unit_id = z["unit_id"]
                                y.qty = z["qty"]
                else:
                    if x["prod_id"] and x["qty"] and x["unit_id"]:
                        new_mutasi.append(
                            MtsiDdb(
                                x.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["qty"],
                            )
                        )

            if len(new_mutasi) > 0:
                db.session.add_all(new_mutasi)

            db.session.commit()

            UpdateMutasi(x.id, False)

            result = response(200, "Berhasil", True, mtsi_schema.dump(x))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Kode sudah digunakan", False, None)
        finally:
            return result
    else:
        UpdateMutasi(mt.id, True)
        old_mutasi = MtsiDdb.query.filter(MtsiDdb.mtsi_id == id).all()
        if old_mutasi:
            for y in old_mutasi:
                db.session.delete(y)

        db.session.delete(x)
        db.session.commit()

        return response(200, "Berhasil", True, None)


@app.route("/v1/api/koreksi-sto", methods=["POST", "GET"])
@token_required
def korSto(self):
    return KoreksiPersediaan(self, request)


@app.route("/v1/api/koreksi-sto/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def korSto_id(self, id):
    return KorPersediaanId(id, request)


@app.route("/v1/api/sto/<int:id>", methods=["GET"])
@token_required
def sto_loc(self, id):
    product = ProdMdb.query.all()
    sto = StCard.query.filter(
        and_(StCard.trx_dbcr == "d", StCard.loc_id == id)).all()

    final = []
    for x in product:
        hrg_pokok = 0
        total_sto = 0
        for y in sto:
            if x.id == y.prod_id:
                total_sto += y.trx_qty
                hrg_pokok += y.trx_hpok

        if total_sto > 0:
            final.append(
                {
                    "id": x.id,
                    "code": x.code,
                    "name": x.name,
                    "group": x.group,
                    "type": x.type,
                    "codeb": x.codeb,
                    "unit": x.unit,
                    "suplier": x.suplier,
                    "b_price": x.b_price,
                    "s_price": x.s_price,
                    "barcode": x.barcode,
                    "metode": x.metode,
                    "max_stock": x.max_stock,
                    "min_stock": x.min_stock,
                    "re_stock": x.re_stock,
                    "lt_stock": x.lt_stock,
                    "max_order": x.max_order,
                    "image": x.image,
                    "stock": total_sto,
                    "hpok": hrg_pokok / total_sto,
                }
            )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/sto", methods=["GET"])
@token_required
def sto(self):
    product = ProdMdb.query.all()
    sto = StCard.query.all()

    # filter(
    #     or_(
    #         and_(StCard.trx_dbcr == "d", StCard.trx_type == "BL"),
    #         and_(StCard.trx_dbcr == "k", StCard.trx_type == "JL"),
    #         and_(StCard.trx_dbcr == "d", StCard.trx_type == "MD"),
    #         and_(StCard.trx_dbcr == "k", StCard.trx_type == "MK"),
    #         and_(StCard.trx_type == "KS"),
    #     )
    # ).

    loc = LocationMdb.query.all()

    final = []
    for z in loc:
        for x in product:
            hrg_pokok = 0
            total_sto = 0
            for y in sto:
                if z.id == y.loc_id:
                    if x.id == y.prod_id:
                        if y.trx_dbcr == "d":
                            total_sto += y.trx_qty
                            # hrg_pokok += y.trx_hpok

                        else:
                            total_sto -= y.trx_qty
                            # hrg_pokok -= y.trx_hpok

            if total_sto > 0:
                final.append(
                    {
                        "id": x.id,
                        "code": x.code,
                        "name": x.name,
                        "group": x.group,
                        "type": x.type,
                        "codeb": x.codeb,
                        "unit": x.unit,
                        "suplier": x.suplier,
                        "b_price": x.b_price,
                        "s_price": x.s_price,
                        "barcode": x.barcode,
                        "metode": x.metode,
                        "max_stock": x.max_stock,
                        "min_stock": x.min_stock,
                        "re_stock": x.re_stock,
                        "lt_stock": x.lt_stock,
                        "max_order": x.max_order,
                        "image": x.image,
                        "stock": total_sto,
                        # "hpok": hrg_pokok / total_sto,
                        "loc_id": z.id,
                    }
                )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/sisa-exp", methods=["GET"])
@token_required
def sisa_exp(self):
    # sld = SaldoAPMdb.query.filter(SaldoAPMdb.id == ApCard.sa_id).all()
    fk = OrdpbHdb.query.all()
    ap = ApCard.query.filter(and_(ApCard.pay_type == "H4")).all()

    final = []
    for x in fk:
        sisa = 0
        sisa_fc = 0
        trx = 0
        acq = 0
        trx_fc = 0
        acq_fc = 0
        # for z in sld:
        for y in ap:
            if x.id == y.ord_id:
                trx = y.trx_amnh
                acq += y.acq_amnh
                trx_fc = y.trx_amnv if y.trx_amnv != None else 0
                acq_fc += y.acq_amnv if y.acq_amnv != None else 0

                sisa = trx - acq
                sisa_fc = trx_fc - acq_fc

                if sisa > 0 or sisa_fc > 0:
                    final.append(
                        {
                            "id": x.id if y.ord_id else None,
                            "fk_code": x.ord_code if y.ord_id else None,
                            "fk_date": x.ord_date if y.ord_id else None,
                            "ord_id": x.id if y.id else None,
                            "sisa": sisa,
                            "sisa_fc": sisa_fc,
                        }
                    )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/sisa-inc", methods=["GET"])
@token_required
def sisa_inc(self):
    sl = OrdpjHdb.query.all()
    # sld = SaldoARMdb.query.all()
    ar = ArCard.query.filter(and_(ArCard.pay_type == "J4")).all()

    final = []
    for x in sl:
        sisa = 0
        sisa_fc = 0
        trx = 0
        acq = 0
        trx_fc = 0
        acq_fc = 0
        # for z in sld:
        for y in ar:
            if x.id == y.bkt_id:
                trx = y.trx_amnh
                acq += y.acq_amnh
                trx_fc = y.trx_amnv if y.trx_amnv != None else 0
                acq_fc += y.acq_amnv if y.acq_amnv != None else 0

        sisa = trx - acq
        sisa_fc = trx_fc - acq_fc

        if sisa > 0:
            final.append(
                {
                    "id": x.id if y.bkt_id else None,
                    "ord_code": x.ord_code if y.bkt_id else None,
                    "ord_date": x.ord_date if y.bkt_id else None,
                    "so_id": x.so_id,
                    "sa_id": None,
                    "pel_id": x.pel_id if y.bkt_id else None,
                    "slsm_id": x.slsm_id,
                    "trx_type": y.trx_type,
                    "sisa": sisa,
                    "sisa_fc": sisa_fc,
                }
            )

        # elif acq:
        #     final.append(
        #         {
        #             "id": x.id,
        #             "ord_code": x.ord_code,
        #             "ord_date": x.ord_date,
        #             "so_id": x.so_id,
        #             "pel_id": x.pel_id,
        #             "slsm_id": x.slsm_id,
        #             "sisa": 0,
        #         }
        #     )

    return response(200, "Berhasil", True, final)


@app.route("/v1/api/koreksi-hut", methods=["POST", "GET"])
@token_required
def korHut(self):
    return KoreksiHutang(self, request)


@app.route("/v1/api/koreksi-hut/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def korHut_id(self, id):
    return KoreksiHutangId(id, request)


@app.route("/v1/api/koreksi-piu", methods=["POST", "GET"])
@token_required
def korPiu(self):
    return KoreksiPiutang(self, request)


@app.route("/v1/api/koreksi-piu/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def korPiu_id(self, id):
    return KoreksiPiutangId(id, request)


@app.route("/v1/api/saldo-awal-inv", methods=["GET", "POST"])
@token_required
def saldo_awal_inv(self):
    return SaldoInv(self, request)


@app.route("/v1/api/saldo-awal-ap", methods=["GET", "POST"])
@token_required
def saldo_awal_ap(self):
    return SaldoAP(self, request)


@app.route("/v1/api/saldo-awal-ap/<int:id>", methods=["PUT", "DELETE"])
@token_required
def sa_ap_id(self, id):
    return SaldoAPId(id, request)


@app.route("/v1/api/saldo-awal-ar", methods=["GET", "POST"])
@token_required
def saldo_awal_ar(self):
    return SaldoAR(self, request)


@app.route("/v1/api/saldo-awal-ar/<int:id>", methods=["PUT", "DELETE"])
@token_required
def sa_ar_id(self, id):
    return SaldoARId(id, request)


@app.route("/v1/api/saldo-awal-gl", methods=["POST", "PUT", "GET"])
@token_required
def saldo_awal_gl(self):
    return SaldoAwalGl(self, request)


@app.route("/v1/api/saldo-awal-gl/status", methods=["GET"])
@token_required
def saldo_awal_status(self):
    return SaldoAwalGlStatus(self, request)


@app.route("/v1/api/setup/saldo-akhir", methods=["POST", "GET"])
@token_required
def setup_sa(self):
    return SetupSldAkhir(self, request)


@app.route("/v1/api/setup/saldo-akhir/<int:id>", methods=["PUT", "GET", "DELETE"])
@token_required
def setup_sa_id(self, id):
    return SetupSaId(id, request, self)


@app.route("/v1/api/saldo-akhir", methods=["POST", "GET"])
@token_required
def saldo_akhir(self):
    return SaldoAkhir(request, self.id, self.company)


@app.route("/v1/api/saldo-akhir/<int:id>", methods=["PUT"])
@token_required
def saldo_akhir_id(self, id):
    return SaldoAkhirId(request, id)


@app.route("/v1/api/posting/ym", methods=["GET"])
@token_required
def get_year(self):
    return GetYearPosting(self, request)


@app.route("/v1/api/posting", methods=["POST", "GET"])
@token_required
def posting(self):
    return Posting(self, request)


@app.route("/v1/api/unpost/<int:month>/<int:year>", methods=["GET"])
@token_required
def unpost(self, month, year):
    return Unpost(self, month, year, request)


@app.route("/v1/api/posting/transfer", methods=["POST"])
@token_required
def tf(self):
    return TransferGL(self, request)


@app.route("/v1/api/closing/<int:month>/<int:year>", methods=["GET"])
@token_required
def closing(self, month, year):
    return Closing(self, month, year, request)
