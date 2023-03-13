from main.model.lokasi_mdb import LocationMdb
from main.model.prod_mdb import ProdMdb
from main.model.sa_inv import SaldoInvMdb
from main.model.user import User
from main.schema.sa_inv import sainv_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.shared.shared import db
from main.utils.response import response
from datetime import datetime, time


class Transfer:
    def __new__(self, user, request):
        users = User.query.filter(User.id == user.id).first()
        if request.method == "POST":
            try:
                loc_id = request.json["loc_id"]
                prod_id = request.json["prod_id"]
                qty = request.json["qty"]
                nilai = request.json["nilai"]
                total = request.json["total"]

                sa = SaldoInvMdb(loc_id, prod_id, qty, nilai, total, user.id)
                db.session.add(sa)
                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, sainv_schema.dump(sa))
        else:
            sld = (
                db.session.query(SaldoInvMdb, LocationMdb, ProdMdb)
                .outerjoin(LocationMdb, LocationMdb.id == SaldoInvMdb.loc_id)
                .outerjoin(ProdMdb, ProdMdb.id == SaldoInvMdb.prod_id)
                .order_by(SaldoInvMdb.id.desc())
                .all()
            )

            final = []
            for x in sld:
                final.append(
                    {
                        "id": x[0].id,
                        "loc_id": loct_schema.dump(x[1]),
                        "prod_id": prod_schema.dump(x[2]),
                        "qty": x[0].qty,
                        "nilai": x[0].nilai,
                        "total": x[0].total,
                        "user_id": x[0].user_id,
                    }
                )

            return response(200, "Berhasil", True, final)

        return response(200, "Berhasil", True, None)
