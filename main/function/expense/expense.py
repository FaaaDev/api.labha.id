from main.function.update_table import UpdateTable
from main.function.update_ap_giro import UpdateApGiro
from main.function.update_ap_payment import UpdateApPayment
from main.function.update_dp_ap import UpdateApDP
from main.model.acq_ddb import AcqDdb
from main.model.bank_mdb import BankMdb
from main.model.comp_mdb import CompMdb
from main.model.exp_ddb import ExpDdb
from main.model.exp_hdb import ExpHdb
from main.model.mukap_ddb import MukapDdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.fkpb_det_ddb import FkpbDetDdb

# from main.model.sa_ap_mdb import SaldoAPMdb
from main.model.giro_hdb import GiroHdb
from main.model.supplier_mdb import SupplierMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.po_mdb import PoMdb
from main.model.user import User
from main.schema.exp_hdb import ExpSchema
from main.model.accou_mdb import AccouMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.bank_mdb import bank_schema
from main.schema.accou_mdb import accou_schema
from main.schema.exp_hdb import exp_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.dexp_ddb import dexp_schema
from main.schema.dacq_ddb import dacq_schema
from main.schema.mukap_ddb import mukap_schema
from main.schema.fkpb_hdb import fkpb_schema
from main.schema.dord_hdb import dord_schema
from main.schema.po_mdb import po_schema

# from main.schema.sa_ap_mdb import saap_schema


class Expense:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                company = (
                    db.session.query(User, CompMdb)
                    .outerjoin(CompMdb, User.company == CompMdb.id)
                    .filter(User.id == user.id)
                    .first()
                )

                exp_code = request.json["exp_code"]
                exp_date = request.json["exp_date"]
                type_trx = request.json["type_trx"]
                acq_sup = request.json["acq_sup"]
                acq_pay = request.json["acq_pay"]
                acq_kas = request.json["acq_kas"]
                bank_ref = request.json["bank_ref"]
                bank_acc = request.json["bank_acc"]
                giro_num = request.json["giro_num"]
                giro_date = request.json["giro_date"]
                bank_id = request.json["bank_id"]
                exp_type = request.json["exp_type"]
                kas_acc = request.json["kas_acc"]
                exp_bnk = request.json["exp_bnk"]
                type_acc = request.json["type_acc"]
                exp_dep = request.json["exp_dep"]
                exp_prj = request.json["exp_prj"]
                dp_type = request.json["dp_type"]
                dp_sup = request.json["dp_sup"]
                dp_kas = request.json["dp_kas"]
                dp_bnk = request.json["dp_bnk"]
                acq = request.json["acq"]
                exp = request.json["exp"]
                det_dp = request.json["det_dp"]

                exps = ExpHdb(
                    exp_code,
                    exp_date,
                    type_trx,
                    acq_sup,
                    acq_pay,
                    acq_kas,
                    bank_ref,
                    bank_acc,
                    giro_num,
                    giro_date,
                    bank_id,
                    exp_type,
                    kas_acc,
                    exp_bnk,
                    type_acc,
                    exp_dep,
                    exp_prj,
                    dp_type,
                    dp_sup,
                    dp_kas,
                    dp_bnk,
                    False if company and company[1].appr_payment else True,
                    user.id,
                )

                db.session.add(exps)
                db.session.commit()

                new_acq = []
                value = 0
                if exps.type_trx == 1:
                    for x in acq:
                        if x["fk_id"] and x["value"] and x["payment"] and x["payment"]:
                            value += x["payment"]
                            new_acq.append(
                                AcqDdb(
                                    exps.id,
                                    x["fk_id"],
                                    x["value"],
                                    x["payment"],
                                    x["dp"],
                                )
                            )

                    if len(new_acq) > 0:
                        db.session.add_all(new_acq)

                elif exps.type_trx == 2:
                    new_exp = []
                    for x in exp:
                        if (x["acc_code"] or x["acc_bnk"] or x["bnk_code"]) and x[
                            "value"
                        ]:
                            new_exp.append(
                                ExpDdb(
                                    exps.id,
                                    x["acc_code"],
                                    x["acc_bnk"],
                                    x["bnk_code"],
                                    x["value"],
                                    x["fc"],
                                    x["desc"],
                                )
                            )

                    if len(new_exp) > 0:
                        db.session.add_all(new_exp)

                else:
                    new_dp = []
                    for x in det_dp:
                        if x["po_id"] and x["value"]:
                            new_dp.append(
                                MukapDdb(
                                    exps.id,
                                    x["po_id"],
                                    x["t_bayar"],
                                    x["value"],
                                    x["remain"],
                                    x["desc"],
                                )
                            )

                    if len(new_dp) > 0:
                        db.session.add_all(new_dp)

                db.session.commit()

                # if company and not company[1].appr_payment:
                #   print("HEHEH")
                if acq_pay and acq_pay == 3:
                    giro = GiroHdb(
                        giro_date,
                        giro_num,
                        bank_id,
                        exps.id,
                        exp_date,
                        acq_sup,
                        value,
                        None,
                        0,
                    )
                    db.session.add(giro)
                    db.session.commit()
                    #     UpdateApGiro(giro.id)

                if type_trx != 3:
                    UpdateApPayment(exps.id, False)
                else:
                    UpdateApDP(exps.id, False)

            except IntegrityError:
                db.session.rollback()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, exp_schema.dump(exps))
        else:
            try:
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
                    db.session.query(AcqDdb, OrdpbHdb).outerjoin(
                        OrdpbHdb, OrdpbHdb.id == AcqDdb.fk_id
                    )
                    # .outerjoin(SaldoAPMdb, SaldoAPMdb.id == AcqDdb.sa_id)
                    # .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbDetDdb.ord_id)
                    .all()
                )

                dp = (
                    db.session.query(MukapDdb, PoMdb).outerjoin(
                        PoMdb, PoMdb.id == MukapDdb.po_id
                    )
                    # .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbDetDdb.ord_id)
                    .all()
                )

                final = []
                for x in exps:

                    all_acq = []
                    for z in acq:
                        if z[0].exp_id == x[0].id:
                            z[0].fk_id = dord_schema.dump(z[1]) if z[1] else None
                            all_acq.append(dacq_schema.dump(z[0]))

                    all_exp = []
                    for y in exp:
                        if y[0].exp_id == x[0].id:
                            all_exp.append(dexp_schema.dump(y[0]))

                    all_dp = []
                    for y in dp:
                        if y[0].exp_id == x[0].id:
                            y[0].po_id = po_schema.dump(y[1])
                            all_dp.append(mukap_schema.dump(y[0]))

                    final.append(
                        {
                            "id": x[0].id,
                            "exp_code": x[0].exp_code,
                            "exp_date": ExpSchema(only=["exp_date"]).dump(x[0])[
                                "exp_date"
                            ],
                            "type_trx": x[0].type_trx,
                            "acq_sup": supplier_schema.dump(x[2]) if x[2] else None,
                            "acq_pay": x[0].acq_pay,
                            "acq_kas": x[0].acq_kas,
                            "bank_ref": x[0].bank_ref,
                            "bank_acc": x[0].bank_acc,
                            "giro_num": x[0].giro_num,
                            "giro_date": ExpSchema(only=["giro_date"]).dump(x[0])[
                                "giro_date"
                            ],
                            "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                            "exp_type": x[0].exp_type,
                            "kas_acc": x[0].kas_acc,
                            "exp_bnk": x[0].exp_bnk,
                            "type_acc": x[0].type_acc,
                            "exp_dep": x[0].exp_dep,
                            "exp_prj": x[0].exp_prj,
                            "dp_type": x[0].dp_type,
                            "dp_sup": x[0].dp_sup,
                            "dp_kas": x[0].dp_kas,
                            "dp_bnk": x[0].dp_bnk,
                            "approve": x[0].approve,
                            "user_id": x[0].user_id,
                            "exp": all_exp,
                            "acq": all_acq,
                            "det_dp": all_dp,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        ExpHdb,
                        BankMdb,
                        SupplierMdb,
                        ExpDdb,
                        AccouMdb,
                        AcqDdb,
                        OrdpbHdb,
                        MukapDdb,
                        PoMdb,
                        GiroHdb,
                    ],
                    request,
                )
