from ...function.update_table import UpdateTable
from ...model.klasi_mdb import KlasiMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.klasi_mdb import klasi_schema, klasies_schema


class Klasifikasi:
    def __new__(self, user, request):
        if request.method == "POST":
            klasi = KlasiMdb(request.json["name"], user.id)
            db.session.add(klasi)
            db.session.commit()
            return response(200, "Berhasil", True, klasi_schema.dump(klasi))
        else:
            try:
                result = KlasiMdb.query.order_by(KlasiMdb.id.asc()).all()

                return response(200, "Berhasil", True, klasies_schema.dump(result))

                klasi = []
                if len(result) == 0:
                    klasi.extend(
                        [
                            KlasiMdb("Assets", user.id),
                            KlasiMdb("Liabilities", user.id),
                            KlasiMdb("Capital", user.id),
                            KlasiMdb("Sales", user.id),
                            KlasiMdb("Purchase", user.id),
                            KlasiMdb("Operational Expense", user.id),
                            KlasiMdb("Expense / Income Other", user.id),
                            KlasiMdb("Expense / Income Extraordinare", user.id),
                            KlasiMdb("Tax", user.id),
                        ]
                    )

                    db.session.add_all(klasi)
                    db.session.commit()

                    return response(
                        200, "Berhasil", True, klasies_schema.dump(klasi)
                    )
            except ProgrammingError as e:
                return UpdateTable([KlasiMdb],request)
