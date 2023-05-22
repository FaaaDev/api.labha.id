from ...function.update_table import UpdateTable
from sqlite3 import *
from ...model.currency_mdb import CurrencyMdb
from ...model.currency_ddb import CurrencyDdb
from ...shared.shared import db
from ...utils.response import response
from ...schema.currency_mdb import currencys_schema, currency_schema


class CurrencyId:
    def __new__(self, id, user_company, request):
        curren = CurrencyMdb.query.filter(CurrencyMdb.id == id).first()
        if request.method == "PUT":
            try:
                curren.code = request.json["code"]
                curren.name = request.json["name"]
                curren.date = request.json["date"]
                curren.rate = request.json["rate"]
                curren.comp_id = user_company
                db.session.commit()
                result = response(200, "Berhasil", True,
                                currency_schema.dump(curren))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        elif request.method == "DELETE":
            db.session.delete(curren)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            return response(200, "Berhasil", True, currency_schema.dump(curren))




               