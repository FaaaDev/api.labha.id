# from main.function.posting.posting_year import GetYearPosting
from main.function.update_table import UpdateTable
from main.model.akhir_mdb import AkhirMdb
from main.model.comp_mdb import CompMdb
from main.model.inv_ddb import InvDdb
from main.model.custom_mdb import CustomerMdb
from main.model.arcard_mdb import ArCard
from main.model.sa_ar_mdb import SaldoARMdb
from main.model.user import User
from main.model.currency_mdb import CurrencyMdb
from main.schema.sa_ar_mdb import saar_schema, SaldoARSchema
from main.schema.custom_mdb import customer_schema
from main.shared.shared import db
from main.utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import *
import requests
import json


class SaldoAR:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                due_date = request.json["due_date"]
                cus_id = request.json["cus_id"]
                type = request.json["type"]
                nilai = request.json["nilai"]

                sa = SaldoARMdb(code, date, due_date, cus_id, type, nilai, user.id)

                db.session.add(sa)
                db.session.commit()

                cp = CompMdb.query.filter(CompMdb.id == user.company).first()

                # today = date.today()


                cus = CustomerMdb.query.filter(CustomerMdb.id == cus_id).first()
                curr = CurrencyMdb.query.all()

                cur_rate = 0
                for y in curr:
                    if y.id == cus.cus_curren:
                        cur_rate = y.rate

                krtar = ArCard(
                    cus_id,
                    code,
                    date,
                    due_date,
                    None,
                    None,
                    None,
                    None,
                    cus.cus_curren,
                    "D" if type != "NK" else "K",
                    "SA",
                    "P1",
                    nilai,
                    nilai / cur_rate if cus.cus_curren != None else 0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    sa.id,
                    True,
                )

                db.session.add(krtar)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                db.session.close()
                print(e)
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, saar_schema.dump(sa))
        else:
            try:
                sld = (
                    db.session.query(SaldoARMdb, CustomerMdb)
                    .outerjoin(CustomerMdb, CustomerMdb.id == SaldoARMdb.cus_id)
                    .order_by(SaldoARMdb.id.desc())
                    .all()
                )

                final = []
                for x in sld:
                    final.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "date": SaldoARSchema(only=["date"]).dump(x[0])["date"],
                            "due_date": SaldoARSchema(only=["due_date"]).dump(x[0])[
                                "due_date"
                            ],
                            "cus_id": customer_schema.dump(x[1]),
                            "type": x[0].type,
                            "nilai": x[0].nilai,
                            "user_id": x[0].user_id,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable([SaldoARMdb, CustomerMdb, ArCard, CompMdb], request)
