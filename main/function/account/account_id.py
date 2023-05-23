from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...model.accou_mdb import AccouMdb
from ...schema.accou_mdb import accou_schema
from ...schema.kateg_mdb import kateg_schema
from ...model.kateg_mdb import KategMdb
from ...schema.klasi_mdb import klasi_schema
from ...model.klasi_mdb import KlasiMdb

class AccountId:
    def __new__(self, id, request):
        account = AccouMdb.query.filter(AccouMdb.id == id).first()
        if request.method == "PUT":
            account.acc_code = request.json["kode_acc"]
            account.acc_name = request.json["acc_name"]
            account.umm_code = request.json["kode_umum"]
            account.kat_code = request.json["kode_kategori"]
            account.dou_type = request.json["du"]
            account.sld_type = request.json["kode_saldo"]
            account.connect = request.json["terhubung"]
            account.sld_awal = request.json["saldo_awal"]
            account.level = request.json["level"]
            db.session.commit()
            

            self.response = response(200, "Berhasil", True, accou_schema.dump(account))
        elif request.method == "DELETE":
            db.session.delete(account)
            db.session.commit()
            

            self.response = response(200, "Berhasil", True, None)
        else:
            result = (
                db.session.query(AccouMdb, KategMdb, KlasiMdb)
                .join(AccouMdb, KategMdb.id == AccouMdb.kat_code)
                .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                .order_by(AccouMdb.acc_code.asc())
                .filter(AccouMdb.id == id)
                .first()
            )
            

            data = {
                "account": accou_schema.dump(result[0]),
                "kategory": kateg_schema.dump(result[1]),
                "klasifikasi": klasi_schema.dump(result[2]),
            }

            self.response = response(200, "Berhasil", True, data)

        return self.response