from ...model.kateg_mdb import KategMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.kateg_mdb import kateg_schema
from ...schema.klasi_mdb import klasi_schema
from ...model.klasi_mdb import KlasiMdb

class KategoryId:
    def __new__(self, id, request):
        kategory = KategMdb.query.filter(KategMdb.id == id).first()
        if request.method == "PUT":
            kategory.name = request.json["name"]
            kategory.kode_klasi = request.json["kode_klasi"]
            kategory.kode_saldo = request.json["kode_saldo"]
            db.session.commit()

            self.response = response(200, "Berhasil", True, kateg_schema.dump(kategory))
        elif request.method == "DELETE":
            db.session.delete(kategory)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            result = (
                db.session.query(KategMdb, KlasiMdb)
                .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                .order_by(KategMdb.id.asc())
                .filter(KategMdb.id == id)
                .first()
            )
            data = {
                "kategory": kateg_schema.dump(result[0]),
                "klasifikasi": klasi_schema.dump(result[1]),
            }

            self.response = response(200, "Berhasil", True, data)

        return self.response