# from ...function.posting.posting_year import GetYearPosting
from ...model.akhir_mdb import AkhirMdb
from ...model.comp_mdb import CompMdb
from ...model.inv_ddb import InvDdb
from ...model.supplier_mdb import SupplierMdb
from ...model.apcard_mdb import ApCard
from ...model.sa_ap_mdb import SaldoAPMdb
from ...model.currency_mdb import CurrencyMdb
from ...model.user import User
from ...schema.sa_ap_mdb import saap_schema, SaldoAPSchema
from ...schema.supplier_mdb import supplier_schema
from ...shared.shared import db
from ...utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import IntegrityError


class SaldoAPId:
    def __new__(self, id, request):
        sa = SaldoAPMdb.query.filter(SaldoAPMdb.id == id).first()
        if request.method == "PUT":
            try:
                sa.code = request.json["code"]
                sa.date = request.json["date"]
                sa.due_date = request.json["due_date"]
                sa.sup_id = request.json["sup_id"]
                sa.type = request.json["type"]
                sa.nilai = request.json["nilai"]

                # cp = CompMdb.query.filter(CompMdb.id == user_company).first()

                # today = date.today()

                sup = SupplierMdb.query.filter(SupplierMdb.id == sa.sup_id).first()
                curr = CurrencyMdb.query.all()

                cur_rate = 0
                for y in curr:
                    if y.id == sup.sup_curren:
                        cur_rate = y.rate

                old_krtap = ApCard.query.filter(ApCard.sa_id == id).first()

                if old_krtap:
                    db.session.delete(old_krtap)

                krtap = ApCard(
                    sa.code,
                    sa.sup_id,
                    None,
                    None,
                    sa.date,
                    sa.due_date,
                    None,
                    None,
                    None,
                    cur_rate if sup.sup_curren != None else None,
                    "k" if sa.type != "ND" else "d",
                    "SA",
                    "P1",
                    sa.nilai,
                    sa.nilai / cur_rate if sup.sup_curren != None else 0,
                    None,
                    None,
                    None,
                    None,
                    sa.id,
                    True,
                )

                db.session.add(krtap)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                db.session.close()
                print(e)
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, saap_schema.dump(sa))

        else:
            old_krtap = ApCard.query.filter(ApCard.sa_id == id).first()
            if old_krtap:
                db.session.delete(old_krtap)

            db.session.delete(sa)
            db.session.commit()

            return response(200, "success", True, None)

        return response(200, "Berhasil", True, None)
