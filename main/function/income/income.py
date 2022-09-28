from main.function.update_ar_giro import UpdateArGiro
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
                inc_type = request.json["inc_type"]
                inc_dep = request.json["inc_dep"]
                inc_acc = request.json["inc_acc"]
                inc_prj = request.json["inc_prj"]
                acq_cus = request.json["acq_cus"]
                acq_pay = request.json["acq_pay"]
                acc_kas = request.json["acc_kas"]
                bank_ref = request.json["bank_ref"]
                bank_id = request.json["bank_id"]
                giro_num = request.json["giro_num"]
                giro_date = request.json["giro_date"]
                giro_bnk = request.json["giro_bnk"]
                acq = request.json["acq"]
                inc = request.json["inc"]

                incs = IncHdb(
                    inc_code,
                    inc_date,
                    inc_type,
                    inc_acc,
                    inc_dep,
                    inc_prj,
                    acq_cus,
                    acq_pay,
                    acc_kas,
                    bank_ref,
                    bank_id,
                    giro_num,
                    giro_date,
                    giro_bnk,
                    None,
                    user.id,
                )

                db.session.add(incs)
                db.session.commit()

                new_inc = []
                for x in inc:
                    if x["acc_code"] and x["value"]:
                        new_inc.append(
                            IncDdb(incs.id, x["acc_code"], x["dbcr"], x["value"], x["desc"])
                        )

                new_acq = []
                value = 0
                for x in acq:
                    if x["sale_id"] and x["value"] and x["payment"] and int(x["payment"]) > 0:
                        value += int(x["payment"])
                        new_acq.append(
                            IAcqDdb(incs.id, x["sale_id"], x["value"], x["payment"])
                        )

                if len(new_inc) > 0:
                    db.session.add_all(new_inc)

                if len(new_acq) > 0:
                    db.session.add_all(new_acq)

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
                        0,
                    )
                    db.session.add(giro)
                    db.session.commit()
                    UpdateArGiro(giro.id)

                    # if acq_pay and acq_pay != 3:
                UpdateArPayment(incs.id, False)

                    

                result = response(200, "Berhasil", True, inc_schema.dump(incs))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result
        else:
            incs = (
                db.session.query(IncHdb, BankMdb, CustomerMdb, AccouMdb)
                .outerjoin(BankMdb, BankMdb.id == IncHdb.bank_id)
                .outerjoin(CustomerMdb, CustomerMdb.id == IncHdb.acq_cus)
                .outerjoin(AccouMdb, AccouMdb.id == IncHdb.inc_acc)
                .order_by(IncHdb.id.desc())
                .all()
            )

            acc = AccouMdb.query.all()

            inc = (
                db.session.query(IncDdb, AccouMdb)
                .outerjoin(AccouMdb, AccouMdb.id == IncDdb.acc_code)
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
                        "giro_date": IncSchema(only=["giro_date"]).dump(x[0])["giro_date"],
                        "giro_bnk": bank_schema.dump(x[1]) if x[1] else None,
                        "approve": x[0].approve,
                        "inc": all_inc,
                        "acq": all_acq,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
