from datetime import datetime
from main.function.update_ar_giro import UpdateArGiro
from main.function.update_dp_ar import UpdateArDP
from main.function.update_ar_payment import UpdateArPayment
from main.model.iacq_ddb import IAcqDdb
from main.model.bank_mdb import BankMdb
from main.model.comp_mdb import CompMdb
from main.model.dinc_ddb import IncDdb
from main.model.inc_hdb import IncHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.giro_inc_hdb import GiroIncHdb
from main.model.custom_mdb import CustomerMdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.sord_hdb import SordHdb
from main.model.mukar_ddb import MukarDdb
from main.model.transddb import TransDdb
from main.model.user import User
from main.model.accou_mdb import AccouMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.bank_mdb import bank_schema
from main.schema.accou_mdb import accou_schema
from main.schema.inc_hdb import IncSchema, inc_schema
from main.schema.custom_mdb import customer_schema
from main.schema.dinc_ddb import dinc_schema
from main.schema.iacq_ddb import iacq_schema
from main.schema.ordpj_hdb import ordpj_schema
from main.schema.dord_hdb import dord_schema
from main.schema.mukar_ddb import mukar_schema
from main.schema.sord_hdb import sord_schema


class Income:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                company = (
                    db.session.query(User, CompMdb)
                    .outerjoin(CompMdb, User.company == CompMdb.id)
                    .filter(User.id == user.id)
                    .first()
                )

                inc_code = request.json["inc_code"]
                inc_date = request.json["inc_date"]
                type_trx = request.json["type_trx"]
                acq_cus = request.json["acq_cus"]
                acq_pay = request.json["acq_pay"]
                acq_kas = request.json["acq_kas"]
                bank_ref = request.json["bank_ref"]
                bank_acc = request.json["bank_acc"]
                giro_num = request.json["giro_num"]
                giro_date = request.json["giro_date"]
                giro_bnk = request.json["giro_bnk"]
                inc_type = request.json["inc_type"]
                inc_kas = request.json["inc_kas"]
                inc_bnk = request.json["inc_bnk"]
                inc_dep = request.json["inc_dep"]
                inc_acc = request.json["inc_acc"]
                inc_prj = request.json["inc_prj"]
                acc_type = request.json["acc_type"]
                dp_type = request.json["dp_type"]
                dp_cus = request.json["dp_cus"]
                dp_kas = request.json["dp_kas"]
                dp_bnk = request.json["dp_bnk"]
                acq = request.json["acq"]
                inc = request.json["inc"]
                det_dp = request.json["det_dp"]

                incs = IncHdb(
                    inc_code,
                    inc_date,
                    type_trx,
                    acq_cus,
                    acq_pay,
                    acq_kas,
                    bank_ref,
                    bank_acc,
                    giro_num,
                    giro_date,
                    giro_bnk,
                    inc_type,
                    inc_kas,
                    inc_bnk,
                    inc_dep,
                    inc_prj,
                    acc_type,
                    dp_type,
                    dp_cus,
                    dp_kas,
                    dp_bnk,
                    None,
                    user.id,
                )

                db.session.add(incs)
                db.session.commit()

                # if giro_bnk:
                #     bank = BankMdb.query.filter(BankMdb.id == giro_bnk).first()

                if incs.type_trx == 2:
                    new_inc = []
                    for x in inc:
                        if (x["acc_code"] or x["acc_bnk"] or x["bnk_code"]) and x["value"]:
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
                    
                    if len(new_inc) > 0:
                        db.session.add_all(new_inc)


                elif incs.type_trx == 1:
                    new_acq = []
                    value = 0
                    for x in acq:
                        if x["sale_id"] and x["value"] and x["payment"] and x["payment"]:
                            value += x["payment"]
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
                        
                    if len(new_acq) > 0:
                        db.session.add_all(new_acq)


                else:
                    new_dp = []
                    for x in det_dp:
                        if x["so_id"] and x["value"]:
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

                    if len(new_dp) > 0:
                        db.session.add_all(new_dp)

                db.session.commit()

                if acq_pay and acq_pay == 3:
                    giro = GiroIncHdb(
                        giro_date,
                        giro_num,
                        incs.giro_bnk,
                        incs.id,
                        inc_date,
                        acq_cus,
                        value,
                        None,
                        0,
                    )

                    db.session.add(giro)
                    db.session.commit()

                if incs.type_trx != 3:
                    UpdateArPayment(incs.id, False)
                else:
                    UpdateArDP(incs.id, False)

                result = response(200, "Berhasil", True, inc_schema.dump(incs))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        else:
            incs = (
                db.session.query(IncHdb, BankMdb, CustomerMdb, AccouMdb)
                .outerjoin(BankMdb, BankMdb.id == IncHdb.bank_acc)
                .outerjoin(CustomerMdb, CustomerMdb.id == IncHdb.acq_cus)
                .outerjoin(AccouMdb, AccouMdb.id == IncHdb.inc_kas)
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
                db.session.query(IAcqDdb, OrdpjHdb).outerjoin(
                    OrdpjHdb, OrdpjHdb.id == IAcqDdb.sale_id
                )
                # .outerjoin(SaldoARMdb, SaldoARMdb.id == IAcqDdb.sa_id)
                .all()
            )

            dp = (
                db.session.query(MukarDdb, SordHdb)
                .outerjoin(SordHdb, SordHdb.id == MukarDdb.so_id)
                .all()
            )

            final = []
            for x in incs:
                all_inc = []
                for y in inc:
                    if y[0].inc_id == x[0].id:
                        all_inc.append(dinc_schema.dump(y[0]))

                all_acq = []
                for z in acq:
                    if z[0].inc_id == x[0].id:
                        z[0].sale_id = ordpj_schema.dump(z[1]) if z[1] else None
                        # z[0].sa_id = saar_schema.dump(z[2]) if z[2] else None
                        all_acq.append(iacq_schema.dump(z[0]))

                all_dp = []
                for z in dp:
                    if z[0].inc_id == x[0].id:
                        z[0].so_id = sord_schema.dump(z[1])
                        all_dp.append(mukar_schema.dump(z[0]))

                final.append(
                    {
                        "id": x[0].id,
                        "inc_code": x[0].inc_code,
                        "inc_date": IncSchema(only=["inc_date"]).dump(x[0])["inc_date"],
                        "type_trx": x[0].type_trx,
                        "acq_cus": customer_schema.dump(x[2]) if x[2] else None,
                        "acq_pay": x[0].acq_pay,
                        "acq_kas": x[0].acq_kas,
                        "bank_ref": x[0].bank_ref,
                        "bank_acc": x[0].bank_acc,
                        "giro_num": x[0].giro_num,
                        "giro_date": IncSchema(only=["giro_date"]).dump(x[0])[
                            "giro_date"
                        ],
                        "giro_bnk": bank_schema.dump(x[1]) if x[1] else None,
                        "inc_type": x[0].inc_type,
                        "inc_kas": x[0].inc_kas,
                        "inc_bnk": x[0].inc_bnk,
                        "inc_dep": x[0].inc_dep,
                        "inc_prj": x[0].inc_prj,
                        "acc_type": x[0].acc_type,
                        "dp_type": x[0].dp_type,
                        "dp_cus": x[0].dp_cus,
                        "dp_kas": x[0].dp_kas,
                        "dp_bnk": x[0].dp_bnk,
                        "approve": x[0].approve,
                        "inc": all_inc,
                        "acq": all_acq,
                        "det_dp": all_dp,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
