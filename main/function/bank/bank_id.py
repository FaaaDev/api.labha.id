from datetime import date
from ...model.accou_ddb import AccouDdb
from ...model.bank_mdb import BankMdb
from ...model.comp_mdb import CompMdb
from ...model.user import User
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.bank_mdb import bank_schema
from ...schema.accou_mdb import accou_schema
from ...model.accou_mdb import AccouMdb


class BankId:
    def __new__(self, user, id, request):
        old_sa = 0
        bank = BankMdb.query.filter(BankMdb.id == id).first()
        if request.method == "PUT":
            # old_sa = bank.sa if bank.sa else 0
            bank.BANK_CODE = request.json["BANK_CODE"]
            bank.acc_id = request.json["ACC_ID"]
            bank.BANK_NAME = request.json["BANK_NAME"]
            bank.CURRENCY = request.json["CURRENCY"] if "CURRENCY" in request.json else None
            bank.BANK_DESC = request.json["BANK_DESC"]
            # bank.sa = request.json["sa"]
            bank.user_edit = user.id
            bank.comp_id = user.company

            db.session.commit()
            

            # old = (
            #     db.session.query(BankMdb, AccouMdb)
            #     .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
            #     .filter(BankMdb.id == id)
            #     .first()
            # )
            

            # company = (
            #     db.session.query(CompMdb)
            #     .filter(CompMdb.id == user.company)
            #     .first()
            # )

            # accddb = AccouDdb.query.filter(AccouDdb.acc_code == old[1].acc_code).first()

            # accddb_all = AccouDdb.query.filter(AccouDdb.sa == True).first()

            # if accddb:
            #     accddb.acc_awal += request.json["sa"] - old_sa
            #     accddb.acc_akhir = accddb.acc_awal
            #     print(accddb.acc_awal)
            #     db.session.commit()
            # else:
            #     new_sa = AccouDdb(
            #         accddb_all.acc_year if accddb_all else date.today().year,
            #         company.cutoff,
            #         old[1].acc_code,
            #         request.json["sa"],
            #         0,
            #         0,
            #         request.json["sa"],
            #         True,
            #         False,
            #         False,
            #         user.id
            #     )

            #     db.session.add(new_sa)
            #     db.session.commit()

            
            self.response = response(200, "Berhasil", True, bank_schema.dump(bank))
        elif request.method == "DELETE":
            db.session.delete(bank)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            result = (
                db.session.query(BankMdb, AccouMdb)
                .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
                .order_by(BankMdb.id.asc())
                .filter(BankMdb.id == id)
                .first()
            )
            
            data = {
                "bank": bank_schema.dump(result[0]),
                "account": accou_schema.dump(result[1]),
            }

            self.response = response(200, "Berhasil", True, data)

        return self.response
