# from ...function.posting.posting_year import GetYearPosting
from ...function.update_table import UpdateTable
from ...model.akhir_mdb import AkhirMdb
from ...model.comp_mdb import CompMdb
from ...model.accou_ddb import AccouDdb
from ...model.user import User
from ...schema.accou_ddb import accddb_schema, accddbs_schema
from ...shared.shared import db
from ...utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import *


class SaldoAwalGl:
    def __new__(self, user, request):
        if request.method == "POST":
            acc = request.json["acc"]
            try:
                new_acc = []
                for x in acc:
                    new_acc.append(
                        AccouDdb(
                            x["acc_year"],
                            x["acc_month"],
                            x["acc_code"],
                            x["acc_awal"],
                            0,
                            0,
                            x["acc_awal"],
                            True,
                            False,
                            False,
                            self.id,
                        )
                    )

                if len(new_acc) > 0:
                    db.session.add_all(new_acc)
                    db.session.commit()

                result = response(200, "Berhasil", True, accddbs_schema.dump(new_acc))
            except IntegrityError:
                db.session.rollback()
                db.session.close()

                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        elif request.method == "PUT":
            old = AccouDdb.query.filter(AccouDdb.sa == True).all()
            acc = request.json["acc"]
            try:
                for x in acc:
                    if x["id"]:
                        for y in old:
                            if x["id"] == y.id:
                                y.acc_awal = x["acc_awal"]
                                y.acc_akhir = x["acc_awal"]

                db.session.commit()

                result = response(200, "Berhasil", True, accddbs_schema.dump(old))
            except IntegrityError:
                db.session.rollback()
                db.session.close()

                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            old = (
                AccouDdb.query.filter(AccouDdb.sa == True)
                .order_by(AccouDdb.acc_code.asc())
                .all()
            )

            return response(200, "Berhasil", True, accddbs_schema.dump(old))

