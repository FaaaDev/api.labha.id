from ...utils.response import response
from ...model.ccost_mdb import CcostMdb
from ...shared.shared import db
from ...schema.ccost_mdb import *
from sqlalchemy.exc import *


class CostCenter:
    def __new__(self, request):
        if request.method == "POST":
            try:
                code = request.json["ccost_code"]
                name = request.json["ccost_name"]
                keterangan = request.json["ccost_ket"]
                cost = CcostMdb(code, name, keterangan)
                db.session.add(cost)
                db.session.commit()
                result = response(200, "Berhasil", True, ccost_schema.dump(cost))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            result = CcostMdb.query.all()

            return response(200, "Berhasil", True, ccosts_schema.dump(result))