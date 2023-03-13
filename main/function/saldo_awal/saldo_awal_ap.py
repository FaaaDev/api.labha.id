# from main.function.posting.posting_year import GetYearPosting
from main.function.update_table import UpdateTable
from main.model.akhir_mdb import AkhirMdb
from main.model.comp_mdb import CompMdb
from main.model.inv_ddb import InvDdb
from main.model.supplier_mdb import SupplierMdb
from main.model.apcard_mdb import ApCard
from main.model.sa_ap_mdb import SaldoAPMdb
from main.model.user import User
from main.model.transddb import TransDdb
from main.model.currency_mdb import CurrencyMdb
from main.schema.sa_ap_mdb import saap_schema, SaldoAPSchema
from main.schema.supplier_mdb import supplier_schema
from main.shared.shared import db
from main.utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import *
import requests
import json


class SaldoAP:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                code = request.json["code"]
                date = request.json["date"]
                due_date = request.json["due_date"]
                sup_id = request.json["sup_id"]
                type = request.json["type"]
                nilai = request.json["nilai"]

                sa = SaldoAPMdb(code, date, due_date, sup_id, type, nilai, user.id)

                db.session.add(sa)
                db.session.commit()

                cp = CompMdb.query.filter(CompMdb.id == user.company).first()

                # today = date.today()


                sup = SupplierMdb.query.filter(SupplierMdb.id == sup_id).first()
                cur = CurrencyMdb.query.all()

                cur_rate = 0
                for y in cur:
                    if y.id == sup.sup_curren:
                        cur_rate = y.rate

                krtap = ApCard(
                    code,
                    sup_id,
                    None,
                    date,
                    due_date,
                    None,
                    None,
                    None,
                    cur_rate if sup.sup_curren != None else None,
                    "k" if type != "ND" else "d",
                    "SA",
                    "P1",
                    nilai,
                    nilai / cur_rate if sup.sup_curren != None else 0,
                    None,
                    None,
                    None,
                    None,
                    sa.id,
                    True,
                )

                db.session.add(krtap)

                # if user.product == "inv+gl":
                #     new_trnas = TransDdb(
                #         code,
                #         date,
                #         sup.sup_uang_muka if type == "ND" else sup.sup_hutang,
                #         None,
                #         None,
                #         None,
                #         sup.sup_curren,
                #         cur_rate,
                #         nilai / cur_rate if sup.sup_curren != None else 0,
                #         nilai,
                #         "D" if type != "NK" else "K",
                #         "JURNAL SALDO AWAL SUPPLIER %s" % (sup.sup_name),
                #         None,
                #         None,
                #     )

                #     db.session.add(new_trnas)
                
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                db.session.close()
                print(e)
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, saap_schema.dump(sa))
        else:
            try:
                sld = (
                    db.session.query(SaldoAPMdb, SupplierMdb)
                    .outerjoin(SupplierMdb, SupplierMdb.id == SaldoAPMdb.sup_id)
                    .order_by(SaldoAPMdb.id.desc())
                    .all()
                )

                # sa = []
                # for x in sld:
                #     sa.append(
                #         InvDdb(
                #             2022,
                #             10,
                #             x[2].id,
                #             x[1].id,
                #             x[0].total,
                #             0,
                #             0,
                #             x[0].total,
                #             x[0].qty,
                #             0,
                #             0,
                #             x[0].qty,
                #             x[0].nilai,
                #             True,
                #             False,
                #             user.id,
                #         )
                #     )

                # db.session.add_all(sa)
                # db.session.commit()

                final = []
                for x in sld:
                    final.append(
                        {
                            "id": x[0].id,
                            "code": x[0].code,
                            "date": SaldoAPSchema(only=["date"]).dump(x[0])["date"],
                            "due_date": SaldoAPSchema(only=["due_date"]).dump(x[0])[
                                "due_date"
                            ],
                            "sup_id": supplier_schema.dump(x[1]),
                            "type": x[0].type,
                            "nilai": x[0].nilai,
                            "user_id": x[0].user_id,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable([SaldoAPMdb, SupplierMdb, CompMdb, ApCard], request)
