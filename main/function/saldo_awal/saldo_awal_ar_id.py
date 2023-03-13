# from main.function.posting.posting_year import GetYearPosting
from main.model.akhir_mdb import AkhirMdb
from main.model.comp_mdb import CompMdb
from main.model.inv_ddb import InvDdb
from main.model.custom_mdb import CustomerMdb
from main.model.arcard_mdb import ArCard
from main.model.sa_ar_mdb import SaldoARMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.user import User
from main.schema.sa_ar_mdb import saar_schema, SaldoARSchema
from main.schema.custom_mdb import customer_schema
from main.shared.shared import db
from main.utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import IntegrityError


class SaldoARId:
    def __new__(self, id, request):
        sa = SaldoARMdb.query.filter(SaldoARMdb.id == id).first()
        if request.method == "PUT":
            try:
                sa.code = request.json["code"]
                sa.date = request.json["date"]
                sa.due_date = request.json["due_date"]
                sa.cus_id = request.json["cus_id"]
                sa.type = request.json["type"]
                sa.nilai = request.json["nilai"]

                # cp = CompMdb.query.filter(CompMdb.id == user.company).first()

                # today = date.today()

                cus = CustomerMdb.query.filter(CustomerMdb.id == sa.cus_id).first()
                curr = CurrencyMdb.query.all()

                old_krtar = ArCard.query.filter(ArCard.sa_id == id).first()

                if old_krtar:
                    db.session.delete(old_krtar)

                cur_rate = 0
                for y in curr:
                    if y.id == cus.cus_curren:
                        cur_rate = y.rate

                krtar = ArCard(
                    sa.cus_id,
                    sa.code,
                    sa.date,
                    sa.due_date,
                    None,
                    None,
                    None,
                    None,
                    cus.cus_curren,
                    "D" if sa.type != "NK" else "K",
                    "SA",
                    "P1",
                    sa.nilai,
                    sa.nilai / cur_rate if cus.cus_curren != None else 0,
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

                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, saar_schema.dump(sa))

        else:
            old_krtar = ArCard.query.filter(ArCard.sa_id == id).first()
            if old_krtar:
                db.session.delete(old_krtar)

            db.session.delete(sa)
            db.session.commit()

            return response(200, "success", True, None)

        return response(200, "Berhasil", True, None)
