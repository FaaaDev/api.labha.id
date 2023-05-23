from ...function.update_table import UpdateTable
from ...model.accou_ddb import AccouDdb
from ...model.bank_mdb import BankMdb
from ...model.comp_mdb import CompMdb
from ...model.user import User
from ...model.currency_mdb import CurrencyMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.bank_mdb import bank_schema
from ...schema.accou_mdb import accou_schema
from ...schema.currency_mdb import currency_schema
from ...model.accou_mdb import AccouMdb
from datetime import date


class Bank:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                BANK_CODE = request.json["BANK_CODE"]
                ACC_ID = request.json["ACC_ID"]
                CURRENCY = request.json["CURRENCY"]
                BANK_NAME = request.json["BANK_NAME"]
                BANK_DESC = request.json["BANK_DESC"]
                # sa = request.json["sa"]

                bank = BankMdb(BANK_CODE, BANK_NAME, BANK_DESC,
                               CURRENCY, ACC_ID, user.id, None, user.company)

                db.session.add(bank)
                db.session.commit()

                # old = (
                #     db.session.query(BankMdb, AccouMdb)
                #     .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
                #     .filter(BankMdb.id == bank.id)
                #     .first()
                # )

                # company = CompMdb.query.filter(
                #     CompMdb.id == user.company).first()

                # accddb = AccouDdb.query.filter(
                #     AccouDdb.acc_code == old[1].umm_code
                # ).first()
                # accddb_all = AccouDdb.query.filter(AccouDdb.sa == True).first()

                # if accddb:
                #     accddb.acc_awal += sa
                #     accddb.acc_akhir += sa
                # else:
                #     new_sa = AccouDdb(
                #         accddb_all.acc_year if accddb_all else date.today().year,
                #         company.cutoff,
                #         old[1].acc_code,
                #         sa,
                #         0,
                #         0,
                #         sa,
                #         True,
                #         False,
                #         False,
                #         user.id,
                #     )

                #     db.session.add(new_sa)

                db.session.commit()

            except Exception as e:
                db.session.rollback()
                db.session.close()
                print(e)
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, bank_schema.dump(bank))
        else:
            try:
                result = (
                    db.session.query(BankMdb, AccouMdb, CurrencyMdb)
                    .outerjoin(AccouMdb, BankMdb.acc_id == AccouMdb.id)
                    .outerjoin(CurrencyMdb, BankMdb.CURRENCY == CurrencyMdb.id)
                    .order_by(BankMdb.id.asc())
                    .all()
                )

                data = [
                    {
                        "bank": bank_schema.dump(x[0]),
                        "account": accou_schema.dump(x[1]),
                        "currency": currency_schema.dump(x[2]),
                    }
                    for x in result
                ]

                return response(200, "Berhasil", True, data)
            except ProgrammingError as e:
                return UpdateTable([BankMdb, AccouMdb, CurrencyMdb, AccouDdb], request)
