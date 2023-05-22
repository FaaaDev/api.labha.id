from ...function.update_table import UpdateTable
from ...model.kateg_mdb import KategMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.kateg_mdb import kateg_schema
from ...schema.klasi_mdb import klasi_schema
from ...model.klasi_mdb import KlasiMdb


class Kategory:
    def __new__(self, user, request):
        if request.method == "POST":
            name = request.json["name"]
            kode_klasi = request.json["kode_klasi"]
            kode_saldo = request.json["kode_saldo"]
            kategory = KategMdb(None, name, kode_klasi,
                                kode_saldo, False, user.id, user.company)
            db.session.add(kategory)
            db.session.commit()

            return response(200, "Berhasil", True, kateg_schema.dump(kategory))
        else:
            try:
                result = (
                    db.session.query(KategMdb, KlasiMdb)
                    .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                    .order_by(KategMdb.kode_klasi.asc())
                    .order_by(KategMdb.id.asc())
                    .all()
                )
                data = [
                    {
                        "kategory": kateg_schema.dump(x[0]),
                        "klasifikasi": klasi_schema.dump(x[1]),
                    }
                    for x in result
                ]

                return response(200, "Berhasil", True, data)
            except ProgrammingError as e:
                return UpdateTable([KategMdb, KlasiMdb], request)
