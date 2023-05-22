from ...model.klasi_mdb import KlasiMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.klasi_mdb import klasi_schema


class KlasifikasiId:
    def __new__(self, id, request):
        klasi = KlasiMdb.query.filter(KlasiMdb.id == id).first()
        klasi.klasiname = request.json["name"]
        db.session.commit()

        self.response = response(200, "Berhasil", True, klasi_schema.dump(klasi))

        return self.response