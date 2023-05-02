from ...function.update_ar_giro import UpdateArGiro
from ...function.update_ar_payment import UpdateArPayment
from ...function.update_dp_ar import UpdateArDP
from ...model.accou_mdb import AccouMdb
from ...model.iacq_ddb import IAcqDdb
from ...model.bank_mdb import BankMdb
from ...model.comp_mdb import CompMdb
from ...model.dinc_ddb import IncDdb
from ...model.inc_hdb import IncHdb
from ...model.mukar_ddb import MukarDdb
from ...model.sord_hdb import SordHdb
from ...model.giro_hdb import GiroHdb
from ...model.custom_mdb import CustomerMdb
from ...model.ordpj_hdb import OrdpjHdb
from ...model.user import User
from ...model.transddb import TransDdb
from ...model.trans_bank import TransBank
from ...schema.accou_mdb import accou_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.bank_mdb import bank_schema
from ...schema.inc_hdb import IncSchema, inc_schema
from ...schema.custom_mdb import customer_schema
from ...schema.dinc_ddb import dinc_schema
from ...schema.iacq_ddb import iacq_schema
from ...schema.mukar_ddb import mukar_schema
from ...schema.ordpj_hdb import ordpj_schema
from ...schema.sord_hdb import sord_schema


class IncomeId:
    def __new__(self, id, request):
        incs = IncHdb.query.filter(IncHdb.id == id).first()
        if request.method == "PUT":
            try:
                inc_code = request.json["inc_code"]
                inc_date = request.json["inc_date"]
                inc_type = request.json["inc_type"]
                inc_dep = request.json["inc_dep"]
                inc_prj = request.json["inc_prj"]
                acq_cus = request.json["acq_cus"]
                acq_pay = request.json["acq_pay"]
                bank_ref = request.json["bank_ref"]
                bank_id = request.json["bank_id"]
                giro_num = request.json["giro_num"]
                giro_date = request.json["giro_date"]
                giro_bnk = request.json["giro_bnk"]
                dp_type = request.json["dp_type"]
                dp_cus = request.json["dp_cus"]
                dp_kas = request.json["dp_kas"]
                dp_bnk = request.json["dp_bnk"]
                acq = request.json["acq"]
                inc = request.json["inc"]
                det_dp = request.json["det_dp"]

                incs.inc_code = inc_code
                incs.inc_date = inc_date
                incs.inc_type = inc_type
                incs.inc_dep = inc_dep
                incs.inc_prj = inc_prj
                incs.acq_cus = acq_cus
                incs.acq_pay = acq_pay
                incs.bank_ref = bank_ref
                incs.bank_id = bank_id
                incs.giro_num = giro_num
                incs.giro_date = giro_date
                incs.giro_bnk = giro_bnk
                incs.dp_type = dp_type
                incs.dp_cus = dp_cus
                incs.dp_kas = dp_kas
                incs.dp_bnk = dp_bnk

                all_inc = IncDdb.query.filter(IncDdb.inc_id == incs.id)
                all_acq = IAcqDdb.query.filter(IAcqDdb.inc_id == incs.id)
                all_dp = IAcqDdb.query.filter(MukarDdb.inc_id == incs.id)

                old_acq = []
                new_acq = []
                for x in acq:
                    for y in all_acq:
                        if x["id"] == y.id:
                            y.sale_id = x["sale_id"]
                            y.sa_id = x["sa_id"]
                            y.value = x["value"]
                            y.payment = x["payment"]
                            y.dp = x["dp"]

                    if x["sale_id"] and x["value"] and x["payment"] and x["payment"]:
                        if x["id"] != 0:
                            old_acq.append(x["id"])
                        else:
                            new_acq.append(
                                IAcqDdb(
                                    incs.id,
                                    x["sale_id"],
                                    x["sa_id"],
                                    x["value"],
                                    x["payment"],
                                    x["dp"],
                                )
                            )

                if len(old_acq) > 0:
                    for x in old_acq:
                        for y in all_acq:
                            if y.id not in old_acq:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in acq:
                                        if z["id"] == x:
                                            y.sale_id = z["sale_id"]
                                            y.sa_id = z["sa_id"]
                                            y.value = z["value"]
                                            y.payment = z["payment"]
                                            y.dp = z["dp"]

                if len(new_acq) > 0:
                    db.session.add_all(new_acq)

                old_inc = []
                new_inc = []
                for x in inc:
                    if x["id"]:
                        if (x["acc_code"] or x["acc_bnk"] or x["bnk_code"]) and x[
                            "value"
                        ]:
                            old_inc.append(x["id"])

                    else:
                        new_inc.append(
                            IncDdb(
                                incs.id,
                                x["acc_code"],
                                x["acc_bnk"],
                                x["bnk_code"],
                                x["value"],
                                x["fc"],
                                x["desc"],
                            )
                        )

                if len(old_inc) > 0:
                    for x in old_inc:
                        for y in all_inc:
                            if y.id not in old_inc:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in inc:
                                        if z["id"] == x:
                                            y.acc_code = z["acc_code"]
                                            y.acc_bnk = z["acc_bnk"]
                                            y.bnk_code = z["bnk_code"]
                                            y.value = z["value"]
                                            y.fc = z["fc"]
                                            y.desc = z["desc"]

                if len(new_inc) > 0:
                    db.session.add_all(new_inc)

                old_dp = []
                new_dp = []
                for x in det_dp:
                    for y in all_dp:
                        if x["id"] == y.id:
                            y.so_id = x["so_id"]
                            y.t_bayar = x["t_bayar"]
                            y.value = x["value"]
                            y.remain = x["remain"]
                            y.desc = x["desc"]

                    if x["so_id"] and x["value"]:
                        if x["id"] != 0:
                            old_dp.append(x["id"])
                        else:
                            new_dp.append(
                                MukarDdb(
                                    incs.id,
                                    x["so_id"],
                                    x["t_bayar"],
                                    x["value"],
                                    x["remain"],
                                    x["desc"],
                                )
                            )

                if len(old_dp) > 0:
                    for x in old_dp:
                        for y in all_dp:
                            if y.id not in old_dp:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in det_dp:
                                        if z["id"] == x:
                                            y.so_id = z["so_id"]
                                            y.t_bayar = z["t_bayar"]
                                            y.value = z["value"]
                                            y.remain = z["remain"]
                                            y.desc = z["desc"]

                if len(new_dp) > 0:
                    db.session.add_all(new_dp)

                db.session.commit()

                if incs.type_trx != 3:
                    UpdateArPayment(incs.id, False)
                else:
                    UpdateArDP(incs.id, False)

                result = response(200, "Berhasil", True, dinc_schema.dump(incs))

            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            if incs.type_trx == 3:
                UpdateArDP(incs.id, True)

            UpdateArPayment(incs.id, True)
            # DeleteApPayment(incs.id)

            inc = IncDdb.query.filter(IncDdb.inc_id == incs.id)
            acq = IAcqDdb.query.filter(IAcqDdb.inc_id == incs.id)
            dp = MukarDdb.query.filter(MukarDdb.inc_id == incs.id)

            for x in inc:
                db.session.delete(x)

            for x in acq:
                db.session.delete(x)

            for x in dp:
                db.session.delete(x)

            old_trans = TransDdb.query.filter(TransDdb.trx_code == incs.inc_code).all()
            if old_trans:
                for y in old_trans:
                    db.session.delete(y)

            old_trans_bank = TransBank.query.filter(
                TransBank.trx_code == incs.inc_code
            ).all()
            if old_trans_bank:
                for y in old_trans_bank:
                    db.session.delete(y)

            db.session.delete(incs)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)

        else:
            incs = (
                db.session.query(IncHdb, BankMdb, CustomerMdb)
                .outerjoin(BankMdb, BankMdb.id == IncHdb.bank_id)
                .outerjoin(CustomerMdb, CustomerMdb.id == IncHdb.acq_cus)
                .order_by(IncHdb.id.desc())
                .all()
            )

            acc = AccouMdb.query.all()

            inc = (
                db.session.query(IncDdb, BankMdb)
                .outerjoin(BankMdb, BankMdb.id == IncDdb.bnk_code)
                .all()
            )

            acq = (
                db.session.query(IAcqDdb, OrdpjHdb)
                .outerjoin(OrdpjHdb, OrdpjHdb.id == IAcqDdb.sale_id)
                .all()
            )

            final = []
            for x in incs:
                all_inc = []
                for y in inc:
                    if y[0].inc_id == x[0].id:
                        y[0].acc_code = accou_schema.dump(y[1])
                        all_inc.append(dinc_schema.dump(y[0]))

                all_acq = []
                for z in acq:
                    if z[0].inc_id == x[0].id:
                        z[0].sale_id = ordpj_schema.dump(z[1])
                        all_acq.append(iacq_schema.dump(z[0]))

                if x[0].inc_acc:
                    for a in acc:
                        if a.id == x[0].inc_acc:
                            x[0].inc_acc = accou_schema.dump(a)

                if x[0].acc_kas:
                    for b in acc:
                        if b.id == x[0].acc_kas:
                            x[0].acc_kas = accou_schema.dump(b)

                final.append(
                    {
                        "id": x[0].id,
                        "inc_code": x[0].inc_code,
                        "inc_date": IncSchema(only=["inc_date"]).dump(x[0])["inc_date"],
                        "inc_type": x[0].inc_type,
                        "inc_acc": accou_schema.dump(x[3]) if x[3] else None,
                        "inc_dep": x[0].inc_dep,
                        "inc_prj": x[0].inc_prj,
                        "acq_cus": customer_schema.dump(x[2]) if x[2] else None,
                        "acq_pay": x[0].acq_pay,
                        "acc_kas": accou_schema.dump(x[3]) if x[3] else None,
                        "bank_ref": x[0].bank_ref,
                        "bank_id": bank_schema.dump(x[1]) if x[1] else None,
                        "giro_num": x[0].giro_num,
                        "giro_date": IncSchema(only=["giro_date"]).dump(x[0])[
                            "giro_date"
                        ],
                        "giro_bnk": bank_schema.dump(x[1]) if x[1] else None,
                        "approve": x[0].approve,
                        "inc": all_inc,
                        "acq": all_acq,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
