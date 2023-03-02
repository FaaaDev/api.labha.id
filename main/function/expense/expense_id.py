from main.function.delete_ap_payment import DeleteApPayment
from main.function.update_ap_giro import UpdateApGiro
from main.function.update_ap_payment import UpdateApPayment
from main.function.update_dp_ap import UpdateApDP
from main.model.transddb import TransDdb
from main.model.acq_ddb import AcqDdb
from main.model.bank_mdb import BankMdb
from main.model.comp_mdb import CompMdb
from main.model.exp_ddb import ExpDdb
from main.model.mukap_ddb import MukapDdb
from main.model.exp_hdb import ExpHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.giro_hdb import GiroHdb
from main.model.apcard_mdb import ApCard
from main.model.supplier_mdb import SupplierMdb
from main.model.user import User
from main.schema.exp_hdb import ExpSchema
from main.model.accou_mdb import AccouMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.bank_mdb import bank_schema
from main.schema.accou_mdb import accou_schema
from main.schema.exp_hdb import exp_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.dexp_ddb import dexp_schema
from main.schema.dacq_ddb import dacq_schema
from main.schema.mukap_ddb import mukap_schema
from main.schema.fkpb_hdb import fkpb_schema


class ExpenseId:
    def __new__(self, id, request):
        exps = ExpHdb.query.filter(ExpHdb.id == id).first()
        if request.method == "PUT":
            try:
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

                exps.exp_code = exp_code
                exps.exp_date = exp_date
                exps.type_trx = type_trx
                exps.acq_sup = acq_sup
                exps.acq_pay = acq_pay
                exps.acq_kas = acq_kas
                exps.bank_ref = bank_ref
                exps.bank_acc = bank_acc
                exps.giro_num = giro_num
                exps.giro_date = giro_date
                exps.bank_id = bank_id
                exps.exp_type = exp_type
                exps.kas_acc = kas_acc
                exps.exp_bnk = exp_bnk
                exps.type_acc = type_acc
                exps.exp_dep = exp_dep
                exps.exp_prj = exp_prj
                exps.dp_type = dp_type
                exps.dp_sup = dp_sup
                exps.dp_kas = dp_kas
                exps.dp_bnk = dp_bnk

                o_acq = AcqDdb.query.filter(AcqDdb.exp_id == exps.id).all()
                o_exp = ExpDdb.query.filter(ExpDdb.exp_id == exps.id).all()
                o_dp = ExpDdb.query.filter(ExpDdb.exp_id == exps.id).all()

                old_acq = []
                new_acq = []
                for x in acq:
                    for y in o_acq:
                        if x["id"] == y.id:
                            y.fk_id = x["fk_id"]
                            y.value = x["value"]
                            y.payment = x["payment"]
                            y.dp = x["dp"]

                    if x["fk_id"] and x["value"] and x["payment"] and x["payment"]:
                        if x["id"] != 0:
                            old_acq.append(x["id"])
                        else:
                            new_acq.append(
                                AcqDdb(
                                    incs.id,
                                    x["fk_id"],
                                    x["value"],
                                    x["payment"],
                                    x["dp"],
                                )
                            )

                if len(old_acq) > 0:
                    for x in old_acq:
                        for y in o_acq:
                            if y.id not in old_acq:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in acq:
                                        if z["id"] == x:
                                            y.fk_id = z["fk_id"]
                                            y.value = z["value"]
                                            y.payment = z["payment"]
                                            y.dp = z["dp"]

                if len(new_acq) > 0:
                    db.session.add_all(new_acq)

                old_exp = []
                new_exp = []
                # for y in o_exp:
                for x in exp:
                    if x["id"]:
                        # if x["id"] == y.id:
                        if (
                            x["acc_code"]
                            or x["acc_bnk"]
                            or x["bnk_code"]
                            and x["value"]
                        ):
                            # y.acc_code = x["acc_code"]
                            # y.acc_bnk = x["acc_bnk"]
                            # y.bnk_code = x["bnk_code"]
                            # y.value = x["value"]
                            # y.fc = x["fc"]
                            # y.desc = x["desc"]

                            old_exp.append(x["id"])

                    else:
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

                if len(old_exp) > 0:
                    for x in old_exp:
                        for y in o_exp:
                            if y.id not in old_exp:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in exp:
                                        if z["id"] == x:
                                            y.acc_code = z["acc_code"]
                                            y.acc_bnk = z["acc_bnk"]
                                            y.bnk_code = z["bnk_code"]
                                            y.value = z["value"]
                                            y.fc = z["fc"]
                                            y.desc = z["desc"]

                if len(new_exp) > 0:
                    db.session.add_all(new_exp)

                old_dp = []
                new_dp = []
                for x in exp:
                    if x["id"]:
                        if x["po_id"] and x["value"]:
                            old_dp.append(x["id"])

                    else:
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

                if len(old_dp) > 0:
                    for x in old_dp:
                        for y in o_dp:
                            if y.id not in old_dp:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in det_dp:
                                        if z["id"] == x:
                                            y.po_id = z["po_id"]
                                            y.t_bayar = z["t_bayar"]
                                            y.value = z["value"]
                                            y.remain = z["remain"]
                                            y.desc = z["desc"]

                if len(new_dp) > 0:
                    db.session.add_all(new_dp)

                db.session.commit()

                if exps.type_trx != 3:
                    UpdateApPayment(id, False)
                else:
                    UpdateApDP(id, False)

                result = response(200, "Berhasil", True, exp_schema.dump(exps))

            except Exception as e:
                print(e)
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            if exps.type_trx == 3:
                UpdateApDP(exps.id, True)

            UpdateApPayment(exps.id, True)
            DeleteApPayment(exps.id)

            exp = ExpDdb.query.filter(ExpDdb.exp_id == exps.id)
            acq = AcqDdb.query.filter(AcqDdb.exp_id == exps.id)
            dp = MukapDdb.query.filter(MukapDdb.exp_id == exps.id)

            for x in acq:
                db.session.delete(x)

            for x in exp:
                db.session.delete(x)

            for x in dp:
                db.session.delete(x)

            old_trans = TransDdb.query.filter(TransDdb.trx_code == exps.exp_code).all()
            if old_trans:
                for y in old_trans:
                    db.session.delete(y)
                    db.session.commit()

            db.session.delete(exps)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            exps = (
                db.session.query(ExpHdb, BankMdb, SupplierMdb)
                .outerjoin(BankMdb, BankMdb.id == ExpHdb.bank_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == ExpHdb.acq_sup)
                .filter(ExpHdb.id == id)
                .all()
            )

            acq = (
                db.session.query(AcqDdb, FkpbHdb)
                .outerjoin(FkpbHdb, FkpbHdb.id == AcqDdb.fk_id)
                .all()
            )

            final = []
            for x in exps:

                all_acq = []
                for z in acq:
                    if z[0].exp_id == x[0].id:
                        z[0].fk_id = fkpb_schema.dump(z[1])
                        all_acq.append(dacq_schema.dump(z[0]))

                final.append(
                    {
                        "id": x[0].id,
                        "exp_code": x[0].exp_code,
                        "exp_date": ExpSchema(only=["exp_date"]).dump(x[0])["exp_date"],
                        # "exp_type": x[0].exp_type,
                        # "exp_bnk": x[0].exp_bnk,
                        # "exp_dep": x[0].exp_dep,
                        # "exp_prj": x[0].exp_prj,
                        "acq_sup": supplier_schema.dump(x[2]) if x[2] else None,
                        "acq_pay": x[0].acq_pay,
                        # "kas_acc": x[0].kas_acc,
                        "bank_acc": x[0].bank_acc,
                        "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                        "bank_ref": x[0].bank_ref,
                        "giro_num": x[0].giro_num,
                        "giro_date": ExpSchema(only=["giro_date"]).dump(x[0])[
                            "giro_date"
                        ],
                        "approve": x[0].approve,
                        "user_id": x[0].user_id,
                        # "exp": all_exp,
                        "acq": all_acq,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
