from ...function.update_table import UpdateTable
from ...model.kateg_mdb import KategMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...schema.kateg_mdb import kateg_schema
from ...schema.klasi_mdb import klasi_schema
from ...model.klasi_mdb import KlasiMdb


class KategoryImport:
    def __new__(self, user, request):
        kateg = request.json["kateg"]

        db.session.query(KategMdb).delete()
        db.session.commit()

        for x in kateg:
            id = x["id"]
            name = x["name"]
            kode_klasi = x["kode_klasi"]
            kode_saldo = x["kode_saldo"]

            try:

                a = KategMdb(id, name, kode_klasi, kode_saldo,
                             True, user.id, user.company)
                db.session.add(a)
                db.session.commit()

            except IntegrityError:
                db.session.rollback()

        return response(200, "Berhasil", True, None)
